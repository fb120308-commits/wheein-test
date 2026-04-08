import streamlit as st
import base64
import pandas as pd
from collections import Counter
from streamlit_gsheets import GSheetsConnection

# --- 1. 檔案處理函數 (整合圖片與音檔) ---
@st.cache_data
def get_base64_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        return ""

# --- 2. Google Sheets 連線設定 ---
# ⚠️ 請務必將下方的網址替換成你瀏覽器網址列看到的完整 Google 試算表網址
SHEET_URL = "https://docs.google.com/spreadsheets/d/18SouKWNtcmN6jt5yOqFq6tbjSUsViBTq8i9k97BhzCc/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

def save_result_to_gsheets(final_type):
    """將測驗結果存入 Google Sheets (解決覆蓋問題版)"""
    try:
        # ttl=0 確保每次寫入前都抓到雲端最新的完整清單，而不是快取資料
        df = conn.read(spreadsheet=SHEET_URL, ttl=0)
        df = df.dropna(how='all')
    except Exception as e:
        # 如果表是空的，建立初始欄位
        df = pd.DataFrame(columns=["timestamp", "result"])

    # 準備新資料
    new_data = pd.DataFrame({
        "timestamp": [pd.Timestamp.now(tz='Asia/Taipei').strftime("%Y-%m-%d %H:%M:%S")], 
        "result": [final_type]
    })
    
    # 執行「接龍」動作：舊資料 + 新資料
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    # 寫回 Google Sheets (請確認你的工作表名稱是否為 "工作表1")
    conn.update(worksheet="工作表1", data=updated_df, spreadsheet=SHEET_URL)

# --- 3. 測驗資料內容 ---
LANG_MAP = {
    "繁體中文": {
        "title": "輝人靈魂視角測驗",
        "select_lang": "請選擇語言 / Select Language",
        "restart_btn": "重新測驗",
        "questions": [
            {"q": "1. 看到輝人發了一張素顏捏臉自拍，妳的反應？", "options": {"A. 尖叫！怎麼會這麼軟萌，好想捏一把！": "A", "B. 覺得表情很逗趣，這角度只有她撐得住。": "B", "C. 眼神依然有戲，透出清冷的氣質。": "C"}},
            {"q": "2. 輝人跟 Ggomo 的互動中，什麼畫面最深刻？", "options": {"A. 輝人跟 Ggomo 說話，牠卻不理她。": "A", "B. 兩者都散發「我行我素」的氛圍。": "B", "C. 抱著 Ggomo 時，溫柔帶點清傲的側臉。": "C"}},
            {"q": "3. 舞台演出中，輝人最吸引你的是？", "options": {"A. 發自內心的享受與開心的笑容。": "A", "B. 旋律即興與獨特的舞台漫步。": "B", "C. 舉手投足間流露出的魅惑感。": "C"}},
            {"q": "4. 你覺得輝人的聲音特質偏向？", "options": {"A. 像午後陽光一樣溫暖治癒。": "A", "B. 像精品咖啡，層次豐富難以捉摸。": "B", "C. 像陳年紅酒，絲滑、迷人且微醺。": "C"}},
            {"q": "5. 看輝人的花絮或綜藝時，你最喜歡她？", "options": {"A. 毫無顧忌的大笑，笑到酒窩深陷。": "A", "B. 突然冒出的四次元發言或吐槽。": "B", "C. 混亂中也能保持優雅成熟的樣子。": "C"}},
            {"q": "6. 談到時尚風格，你覺得她最能駕馭？", "options": {"A. Oversized Boylish 風衛衣與鴨舌帽。": "A", "B. 色彩鮮豔、剪裁奇特的街頭塗鴉風。": "B", "C. 貼身西裝外套，展現幹練與神祕感。": "C"}},
            {"q": "7. 如果演唱會最後可以點一首歌，你會選？", "options": {"A. 〈Wheee〉": "A", "B. 〈EASY〉 (ft. Sik-K)": "B", "C. 〈Shhh〉": "C"}},
            {"q": "8. 你覺得輝人的刺青代表她的？", "options": {"A. 對生活的純真熱愛與自由渴望。": "A", "B. 藝術家靈魂，帶點怪誕的美。": "B", "C. 成熟、神祕，像一個有故事的女人。": "C"}},
            {"q": "9. 在團體舞台中，輝人的角色是？", "options": {"A. 連結成員情感的暖心甜心。": "A", "B. 帶來驚喜、讓舞台更有趣的鬼才。": "B", "C. 增添靈魂爵士與性感氣場的關鍵。": "C"}},
            {"q": "10. 你覺得輝人的眼睛最常透露？", "options": {"A. 「我們來玩吧！」": "A", "B. 「你在想什麼？」": "B", "C. 「看著我。」": "C"}}
        ],
        "results": {
            "A": {"type": "狗派：可愛元氣", "desc": "在你眼裡，輝人就是那個「定式可愛」的代表。你最容易被她的笑容、酒窩和親和力擊倒。"},
            "B": {"type": "貓派：古靈精怪", "desc": "你最欣賞輝人的藝術家氣質。在她身上你看到高傲卻好奇的靈魂。"},
            "C": {"type": "狐狸派：極致性感", "desc": "你完全沉溺於輝人的舞台魅力與成熟風情。在她身上散發出致命的優雅。"}
        }
    },
    "한국어": {
        "title": "【휘인 소울 시각 테스트】",
        "select_lang": "언어를 선택하세요",
        "restart_btn": "다시 하기",
        "questions": [
            {"q": "1. 휘인이 민낯으로 볼을 꼬집으며 찍은 셀카를 올렸을 때 반응은?", "options": {"A. 심쿵! 어쩜 이렇게 말랑콩떡 같지?": "A", "B. 표정이 너무 익살스럽네.": "B", "C. 민낯인데도 눈빛이 깊네.": "C"}},
            # ... 此處可依格式補全其餘韓文題目
        ],
        "results": {
            "A": {"type": "강아지파", "desc": "당신의 눈에 휘인은 '정석 귀요미' 그 자체입니다."},
            "B": {"type": "고양이파", "desc": "당신은 휘인의 예술가적 기질을 가장 아낍니다."},
            "C": {"type": "여우파", "desc": "당신은 휘인의 무대 위 아우라에 완전히 빠져 있습니다."}
        }
    },
    "English": {
        "title": "Whee In Soul Quiz",
        "select_lang": "Select Language",
        "restart_btn": "Restart",
        "questions": [
            {"q": "1. Whee In's bare-faced selfie pinching her cheeks, your reaction?", "options": {"A. AHH! So soft and squishy!": "A", "B. Hilarious angle.": "B", "C. Chic aura.": "C"}},
            # ... 此處可依格式補全其餘英文題目
        ],
        "results": {
            "A": {"type": "Puppy Type", "desc": "In your eyes, Whee In is the definition of 'Standard Cuteness.'"},
            "B": {"type": "Cat Type", "desc": "You admire her artistic temperament and 'one-of-a-kind' soul."},
            "C": {"type": "Fox Type", "desc": "You're completely immersed in her stage presence and mature allure."}
        }
    }
}

# --- 4. CSS 樣式設定 (美化介面) ---
img_header = get_base64_file("Header.png")
img_middle = get_base64_file("Middle.png")
img_footer = get_base64_file("Footer.png")

bg_header = f'url("data:image/png;base64,{img_header}")' if img_header else "none"
bg_middle = f'url("data:image/png;base64,{img_middle}")' if img_middle else "none"
bg_footer = f'url("data:image/png;base64,{img_footer}")' if img_footer else "none"

st.markdown(f"""
    <style>
    header {{ visibility: hidden !important; height: 0px !important; }}
    .stApp {{ 
        background-color: #9d2933;
        background-image: {bg_header}, {bg_footer}, {bg_middle} !important;
        background-position: top center, bottom center, top center !important;
        background-repeat: no-repeat, no-repeat, repeat-y !important;
        background-size: min(100%, 420px) auto !important; 
    }}
    .block-container {{
        max-width: 420px !important; 
        margin: auto; 
        padding: 280px 20px 300px 20px !important; 
    }}
    h1, h2, h3 {{ color: #3d1b1b !important; text-align: center; }}
    .stMarkdown p {{
        background-color: rgba(255, 255, 255, 0.6);
        padding: 8px 15px !important; border-radius: 10px; color: #333333 !important;
    }}
    .stButton > button {{ 
        width: 100%; border-radius: 12px; background: white; color: #b71c1c; 
        font-weight: bold; border: 1.5px solid #b71c1c; margin-bottom: 5px;
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
        <div style="position: relative; z-index: 999; top: -150px; left: -10px; height: 0px;">
            <audio controls autoplay loop style="height: 35px; width: 230px; opacity: 0.8; border-radius: 20px;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 6. 流程控制 ---
if 'step' not in st.session_state: st.session_state.step = -1
if 'answers' not in st.session_state: st.session_state.answers = []
if 'lang' not in st.session_state: st.session_state.lang = "繁體中文"
if 'recorded' not in st.session_state: st.session_state.recorded = False

curr_data = LANG_MAP.get(st.session_state.lang, LANG_MAP["繁體中文"])

# A. 語言選擇畫面
if st.session_state.step == -1:
    st.markdown("### Select Language")
    col1, col2, col3 = st.columns(3)
    if col1.button("繁體中文", use_container_width=True):
        st.session_state.lang, st.session_state.step = "繁體中文", 0
        st.rerun()
    if col2.button("한국어", use_container_width=True):
        st.session_state.lang, st.session_state.step = "한국어", 0
        st.rerun()
    if col3.button("English", use_container_width=True):
        st.session_state.lang, st.session_state.step = "English", 0
        st.rerun()

# B. 題目進行畫面
elif st.session_state.step < len(curr_data["questions"]):
    q_item = curr_data["questions"][st.session_state.step]
    st.write(f"**{q_item['q']}**")
    for text, val in q_item["options"].items():
        if st.button(text, key=f"btn_{st.session_state.step}_{val}"):
            st.session_state.answers.append(val)
            st.session_state.step += 1
            st.rerun()

# C. 結果顯示畫面
else:
    counts = Counter(st.session_state.answers)
    top_choice = counts.most_common(1)[0][0]
    res = curr_data["results"][top_choice]
    
    # 儲存結果到 Google Sheets (只儲存一次)
    if not st.session_state.recorded:
        with st.spinner('Calculating...'):
            save_result_to_gsheets(res['type'])
        st.session_state.recorded = True

    st.balloons()
    st.markdown(f"""
        <div class='result-box'>
            <h2>{res['type']}</h2>
            <p>{res['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # 間隔
    if st.button(curr_data["restart_btn"], use_container_width=True):
        st.session_state.step = -1
        st.session_state.answers = []
        st.session_state.recorded = False
        st.rerun()
