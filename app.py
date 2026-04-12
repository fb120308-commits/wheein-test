import streamlit as st
import base64
import pandas as pd
from collections import Counter
from streamlit_gsheets import GSheetsConnection

# --- 1. 檔案處理函數 ---
@st.cache_data
def get_base64_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        return ""

# --- 2. Google Sheets 連線與儲存設定 ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/18SouKWNtcmN6jt5yOqFq6tbjSUsViBTq8i9k97BhzCc/edit?gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

def save_result_to_gsheets(final_type):
    try:
        existing_df = conn.read(spreadsheet=SHEET_URL, ttl=0)
        if existing_df is not None:
            existing_df = existing_df.dropna(how='all')
        else:
            existing_df = pd.DataFrame(columns=["timestamp", "result"])
    except Exception as e:
        return

    new_row = pd.DataFrame({
        "timestamp": [pd.Timestamp.now(tz='Asia/Taipei').strftime("%Y-%m-%d %H:%M:%S")], 
        "result": [final_type]
    })
    
    updated_df = pd.concat([existing_df, new_row], ignore_index=True)
    try:
        conn.update(worksheet="工作表1", data=updated_df, spreadsheet=SHEET_URL)
    except Exception as e:
        pass

# --- 3. 測驗資料內容 (根據 PDF 更新) ---
LANG_MAP = {
    "繁體中文": {
        "title": "輝人靈魂視角測驗",
        "select_lang": "請選擇語言 / Select Language",
        "restart_btn": "重新測驗",
        "questions": [
            {"q": "1. 看到輝人發了一張自拍，你的反應是？", "options": {"A. 尖叫！怎麼那麼可愛！好想捏": "A", "B. 果然是丁輝人，這個角度只有她撐得住": "B", "C. 眼神好深邃，好有氣質": "C"}},
            {"q": "2. 哪一張圖片最能代表你心目中輝人和 Ggomo 的互動？", "options": {"A. 溫馨陪伴的日常": "A", "B. 互相嫌棄卻離不開彼此": "B", "C. 高冷且優雅的對視": "C"}},
            {"q": "3. 舞台演出中，輝人最吸引你的是？", "options": {"A. 發自內心的享受與開心的笑容": "A", "B. 即興的舞步、talking 時突然的撒嬌": "B", "C. 舉手投足間流露出的魅力、流暢的跳舞線條": "C"}},
            {"q": "4. 輝人的聲音是...", "options": {"A. 午後陽光，溫暖且療癒": "A", "B. 特調咖啡，層次豐富難以捉摸": "B", "C. 陳年紅酒，絲滑迷人且微醺": "C"}},
            {"q": "5. 看幕後花絮或綜藝時，你最喜歡輝人...", "options": {"A. 毫無顧忌地大笑，笑到酒窩深陷": "A", "B. 每次和團員玩遊戲都是贏家": "B", "C. 混亂中卻展現出成熟的樣子": "C"}},
            {"q": "6. 你覺得輝人最能夠駕馭...", "options": {"A. Oversized 上衣與全封帽": "A", "B. 鮮豔色彩的藝術塗鴉風": "B", "C. 幹練神祕的西裝造型": "C"}},
            {"q": "7. 你覺得輝人的眼神最常透露...", "options": {"A. 純真且充滿好奇心": "A", "B. 搞怪且難以捉摸": "B", "C. 誘惑且充滿故事": "C"}},
            {"q": "8. 如果演唱會最後只能再聽一首歌，你會選...", "options": {"A. 〈Wheee〉": "A", "B. 〈EASY〉": "B", "C. 〈Shhh〉": "C"}},
            {"q": "9. 你覺得輝人的刺青代表她的...", "options": {"A. 對生活的純真熱愛": "A", "B. 藝術家靈魂": "B", "C. 充滿故事的過往": "C"}},
            {"q": "10. 在 Mamamoo 裡，輝人是...", "options": {"A. 眾人愛的團寵": "A", "B. 帶來驚喜的鬼才": "B", "C. 團體的棟樑": "C"}}
        ],
        "results": {
            "A": {"type": "Puppy", "desc": "Whee, in my world, is a Puppy!"},
            "B": {"type": "Cat", "desc": "Whee, in my world, is a Cat!"},
            "C": {"type": "Fox", "desc": "Whee, in my world, is a Fox!"}
        }
    }
}

# --- 4. 狀態管理與 CSS ---
if 'step' not in st.session_state: st.session_state.step = -2
if 'answers' not in st.session_state: st.session_state.answers = []
if 'lang' not in st.session_state: st.session_state.lang = "繁體中文"
if 'recorded' not in st.session_state: st.session_state.recorded = False

img_header = get_base64_file("Header.png")
img_middle = get_base64_file("Middle.png")
img_footer = get_base64_file("Footer.png")
img_start = get_base64_file("Start screen.png")

if st.session_state.step == -2:
    current_bg = f'url("data:image/png;base64,{img_start}")' if img_start else "none"
    bg_settings = f"""
        background-image: {current_bg} !important;
        background-position: top center !important;
        background-repeat: no-repeat !important;
        background-size: 100% auto !important;
    """
    custom_btn_style = """
        .stButton > button {
            position: fixed;
            top: 0; left: 0;
            width: 100vw !important;
            height: 100vh !important;
            opacity: 0 !important;
            z-index: 9999;
            border: none !important;
            cursor: pointer;
        }
    """
else:
    bg_h = f'url("data:image/png;base64,{img_header}")' if img_header else "none"
    bg_f = f'url("data:image/png;base64,{img_footer}")' if img_footer else "none"
    bg_m = f'url("data:image/png;base64,{img_middle}")' if img_middle else "none"
    bg_settings = f"""
        background-image: {bg_h}, {bg_f}, {bg_m} !important;
        background-position: top center, bottom center, top center !important;
        background-repeat: no-repeat, no-repeat, repeat-y !important;
        background-size: min(100%, 420px) auto !important;
    """
    custom_btn_style = ""

st.markdown(f"""
    <style>
    header {{ visibility: hidden !important; height: 0px !important; }}
    .stApp {{ 
        background-color: #9d2933;
        {bg_settings}
    }}
    .block-container {{
        max-width: 420px !important; 
        margin: auto; 
        padding: 280px 20px 300px 20px !important;
    }}
    {custom_btn_style}
    .stButton > button {{ 
        width: 100%; border-radius: 12px; background: white; color: #b71c1c; 
        font-weight: bold; border: 1.5px solid #b71c1c; margin-bottom: 5px;
    }}
    .stMarkdown p {{
        background-color: rgba(255, 255, 255, 0.6);
        padding: 8px 15px !important; 
        border-radius: 10px; 
        color: #333333 !important;
    }}
    .result-box {{ 
        background: rgba(255,255,255,0.9); padding: 20px; border-radius: 20px; 
        text-align: center; color: black; border: 2px solid #b71c1c;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. 背景音樂 ---
audio_base64 = get_base64_file("bgm.mp3")
if audio_base64:
    audio_html = f"""
        <div style="position: fixed; z-index: 10000; top: 15px; left: 15px; height: 0px;">
            <audio controls autoplay loop style="height: 35px; width: 44px; opacity: 0.7; border-radius: 50%;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 6. 流程控制 ---
curr_data = LANG_MAP.get(st.session_state.lang, LANG_MAP["繁體中文"])

if st.session_state.step == -2:
    if st.button("CLICK_TO_START"):
        st.session_state.step = -1
        st.rerun()

elif st.session_state.step == -1:
    st.markdown(f"### {curr_data['select_lang']}")
    col1, col2, col3 = st.columns(3)
    if col1.button("繁體中文", use_container_width=True):
        st.session_state.lang, st.session_state.step = "繁體中文", 0
        st.rerun()
    # 韓國語和英文暫時共用中文題目邏輯，如有翻譯需求可再調整
    if col2.button("한국어", use_container_width=True):
        st.session_state.lang, st.session_state.step = "繁體中文", 0
        st.rerun()
    if col3.button("English", use_container_width=True):
        st.session_state.lang, st.session_state.step = "繁體中文", 0
        st.rerun()

elif st.session_state.step < len(curr_data["questions"]):
    q_item = curr_data["questions"][st.session_state.step]
    st.write(f"**{q_item['q']}**")
    for text, val in q_item["options"].items():
        if st.button(text, key=f"btn_{st.session_state.step}_{val}"):
            st.session_state.answers.append(val)
            st.session_state.step += 1
            st.rerun()

else:
    counts = Counter(st.session_state.answers)
    top_choice = counts.most_common(1)[0][0]
    res = curr_data["results"][top_choice]
    if not st.session_state.recorded:
        save_result_to_gsheets(res['type'])
        st.session_state.recorded = True
    st.balloons()
    st.markdown(f"""
        <div class='result-box'>
            <h2>{res['type']}</h2>
            <p>{res['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button(curr_data["restart_btn"], use_container_width=True):
        st.session_state.step = -1
        st.session_state.answers = []
        st.session_state.recorded = False
        st.rerun()
