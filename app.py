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

# --- 3. 測驗資料內容 (修正第二題與第六題圖片檔名) ---
LANG_MAP = {
    "繁體中文": {
        "title": "輝人靈魂視角測驗",
        "select_lang": "請選擇語言 / Select Language",
        "restart_btn": "重新測驗",
        "questions": [
            {"q": "1. 看到輝人發了一張自拍，你的反應是？", "options": {"A. 尖叫！怎麼那麼可愛！好想捏": "A", "B. 果然是丁輝人，這個角度只有她撐得住": "B", "C. 眼神好深邃，好有氣質": "C"}},
            {
                "q": "2. 哪一張圖片最能代表你心目中輝人和Ggomo的互動？", 
                "options": {"A": "A", "B": "B", "C": "C"},
                "images": {"A": "q2_A.jpg", "B": "q2_B.jpg", "C": "q2_C.jpg"} 
            },
            {"q": "3. 舞台演出中，輝人最吸引你的是？", "options": {"A. 發自內心的享受與開心的笑容": "A", "B. 即興的舞步、talking 時突然的撒嬌": "B", "C. 舉手投足間流露出的魅力、流暢的跳舞線條": "C"}},
            {"q": "4. 輝人的聲音是...", "options": {"A. 午後陽光，溫暖且療癒": "A", "B. 特調咖啡，層次豐富難以捉摸": "B", "C. 陳年紅酒，絲滑迷人且微醺": "C"}},
            {"q": "5. 看幕後花絮或綜藝時，你最喜歡輝人...", "options": {"A. 毫無顧忌地大笑，笑到酒窩深陷": "A", "B. 每次和團員玩遊戲都是贏家": "B", "C. 混亂中卻展現出成熟的樣子": "C"}},
            {
                "q": "6. 你覺得輝人最能夠駕馭...", 
                "options": {"A": "A", "B": "B", "C": "C"},
                "images": {"A": "q6_A.jpg", "B": "q6_B.jpg", "C": "q6_C.jpg"}
            },
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
    },
    "한국어": {
        "title": "【휘인 소울 시각 테스트】",
        "select_lang": "언어를 선택하세요",
        "restart_btn": "다시 하기",
        "questions": [
            {"q": "1. 휘인이 셀카를 올린 것을 봤을 때, 당신의 반응은?", "options": {"A. 꺄악! 어쩜 이렇게 귀여워! 꼬집어주고 싶어.": "A", "B. 역시 정휘인, 이 각도는 그녀만 소화할 수 있지.": "B", "C. 눈빛이 너무 깊고, 분위기 있어.": "C"}},
            {
                "q": "2. 당신이 생각하는 휘인과 꼬모(Ggomo)의 상호작용을 가장 잘 나타내는 사진은?", 
                "options": {"A": "A", "B": "B", "C": "C"},
                "images": {"A": "q2_A.jpg", "B": "q2_B.jpg", "C": "q2_C.jpg"}
            },
            {"q": "3. 무대 할 때 휘인에게 가장 끌리는 점은?", "options": {"A. 진심으로 즐기는 모습과 행복한 미소.": "A", "B. 즉흥적인 춤, 토크 중 갑작스러운 애교.": "B", "C. 일거수일투족에서 묻어나는 매력, 부드러운 춤선.": "C"}},
            {"q": "4. 휘인의 목소리는...", "options": {"A. 오후의 햇살, 따뜻하고 힐링 돼.": "A", "B. 스페셜티 커피, 다채로운 매력에 예측할 수 없어.": "B", "C. 숙성된 와인, 실크처럼 부드럽고 매혹적이며 살짝 취하게 해.": "C"}},
            {"q": "5. 비하인드 영상이나 예능을 볼 때, 당신이 가장 좋아하는 휘인의 모습은...", "options": {"A. 보조개가 깊게 파일 정도로 거침없이 크게 웃을 때.": "A", "B. 멤버들과 게임할 때마다 항상 승자가 될 때.": "B", "C. 혼란스러운 와중에도 성숙한 모습을 보여줄 때.": "C"}},
            {
                "q": "6. 당신이 생각하기에 휘인이 가장 잘 소화하는 스타일은...", 
                "options": {"A": "A", "B": "B", "C": "C"},
                "images": {"A": "q6_A.jpg", "B": "q6_B.jpg", "C": "q6_C.jpg"}
            },
            {"q": "7. 당신이 생각하기에 휘인의 눈빛이 가장 자주 보여주는 것은...", "options": {"A. 순수하고 호기심 가득한 모습": "A", "B. 엉뚱하고 종잡을 수 없는 모습": "B", "C. 매혹적이고 사연 있어 보이는 모습": "C"}},
            {"q": "8. 콘서트 마지막에 딱 한 곡만 더 들을 수 있다면, 당신의 선택은...", "options": {"A. 〈Wheee〉": "A", "B. 〈EASY〉": "B", "C. 〈Shhh〉": "C"}},
            {"q": "9. 휘인의 타투가 의미하는 것은...", "options": {"A. 삶에 대한 순수한 사랑과 열정.": "A", "B. 아티스트의 영혼.": "B", "C. 이야기로 가득 찬 과거.": "C"}},
            {"q": "10. 마마무에서 휘인은...", "options": {"A. 모두의 사랑을 독차지하는 사랑둥이.": "A", "B. 놀라움을 안겨주는 천재.": "B", "C. 그룹의 든든한 기둥.": "C"}}
        ],
        "results": {
            "A": {"type": "Puppy", "desc": "Whee, in my world, is a Puppy!"},
            "B": {"type": "Cat", "desc": "Whee, in my world, is a Cat!"},
            "C": {"type": "Fox", "desc": "Whee, in my world, is a Fox!"}
        }
    },
    "English": {
        "title": "Whee In Soul Quiz",
        "select_lang": "Select Language",
        "restart_btn": "Restart",
        "questions": [
            {"q": "1. What is your reaction when you see Wheein post a selfie?", "options": {"A. Wow! How can she be so cute! I want to pinch her cheeks.": "A", "B. As expected of Jung Wheein, only she can pull off this angle.": "B", "C. Her eyes are so deep and elegant.": "C"}},
            {
                "q": "2. Which picture best represents the interaction between Wheein and Ggomo in your mind?", 
                "options": {"A": "A", "B": "B", "C": "C"},
                "images": {"A": "q2_A.jpg", "B": "q2_B.jpg", "C": "q2_C.jpg"}
            },
            {"q": "3. What attracts you most about Wheein during stage performances?", "options": {"A. Her genuine enjoyment and happy smile.": "A", "B. Impromptu dance moves, and her sudden aegyo during talking segments.": "B", "C. The charm exuded in her every move, and her smooth dance lines.": "C"}},
            {"q": "4. Wheein's voice is...", "options": {"A. Afternoon sunshine, warm and healing": "A", "B. Specialty coffee, richly layered and unpredictable.": "B", "C. Aged red wine, silky, charming, and slightly intoxicating.": "C"}},
            {"q": "5. When watching behind-the-scenes or variety shows, you like it most when Wheein...", "options": {"A. Laughs out loud without holding back, showing off her deep dimples.": "A", "B. Ends up being the winner every time she plays games with the members.": "B", "C. Shows her mature side amidst the chaos.": "C"}},
            {
                "q": "6. What do you think Wheein can pull off the best...", 
                "options": {"A": "A", "B": "B", "C": "C"},
                "images": {"A": "q6_A.jpg", "B": "q6_B.jpg", "C": "q6_C.jpg"}
            },
            {"q": "7. What do you think Wheein's eyes most often reveal...", "options": {"A. Pure and full of curiosity": "A", "B. Quirky and unpredictable": "B", "C. Alluring and full of stories": "C"}},
            {"q": "8. If you could only listen to one last song at the end of a concert, you would choose...", "options": {"A. 〈Wheee〉": "A", "B. 〈EASY〉": "B", "C. 〈Shhh〉": "C"}},
            {"q": "9. What do you think Wheein's tattoos represent...", "options": {"A. Her innocent love for life.": "A", "B. Her artistic soul.": "B", "C. A past full of stories.": "C"}},
            {"q": "10. In Mamamoo, Wheein is...", "options": {"A. The beloved group pet everyone adores.": "A", "B. A genius who always brings surprises.": "B", "C. The reliable pillar of the group.": "C"}}
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
    if col2.button("한국어", use_container_width=True):
        st.session_state.lang, st.session_state.step = "한국어", 0
        st.rerun()
    if col3.button("English", use_container_width=True):
        st.session_state.lang, st.session_state.step = "English", 0
        st.rerun()

elif st.session_state.step < len(curr_data["questions"]):
    q_item = curr_data["questions"][st.session_state.step]
    st.write(f"**{q_item['q']}**")
    
    # 圖片選項顯示邏輯
    has_images = "images" in q_item
    cols = st.columns(len(q_item["options"]))
    
    for idx, (text, val) in enumerate(q_item["options"].items()):
        with cols[idx]:
            # 如果這題有圖片，在按鈕上方顯示圖片
            if has_images and val in q_item["images"]:
                # 讀取 JPG 檔案
                image_base64 = get_base64_file(q_item["images"][val])
                if image_base64:
                    st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 5px;">
                            <img src="data:image/jpeg;base64,{image_base64}" style="max-width: 100%; height: auto; border-radius: 10px;">
                        </div>
                    """, unsafe_allow_html=True)
            
            # 顯示按鈕
            if st.button(text, key=f"btn_{st.session_state.step}_{val}", use_container_width=True):
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
