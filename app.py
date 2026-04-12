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
    """將測驗結果存入 Google Sheets"""
    try:
        # 1. 讀取現有資料
        existing_df = conn.read(spreadsheet=SHEET_URL, ttl=0)
        
        # 2. 清理無效行
        if existing_df is not None:
            existing_df = existing_df.dropna(how='all')
        else:
            existing_df = pd.DataFrame(columns=["timestamp", "result"])
            
    except Exception as e:
        return

    # 3. 準備新資料
    new_row = pd.DataFrame({
        "timestamp": [pd.Timestamp.now(tz='Asia/Taipei').strftime("%Y-%m-%d %H:%M:%S")], 
        "result": [final_type]
    })
    
    # 4. 接龍更新
    updated_df = pd.concat([existing_df, new_row], ignore_index=True)
    
    # 5. 寫回雲端
    try:
        conn.update(worksheet="工作表1", data=updated_df, spreadsheet=SHEET_URL)
    except Exception as e:
        pass

# --- 3. 測驗資料內容 (保持不變) ---
LANG_MAP = {
    "繁體中文": {
        "title": "輝人靈魂視角測驗",
        "select_lang": "請選擇語言 / Select Language",
        "restart_btn": "重新測驗",
        "questions": [
            {"q": "1. 看到輝人發了一張素顏捏臉自拍，妳的反應？", "options": {"A. 尖叫！怎麼會這麼軟萌，好想捏一把！": "A", "B. 覺得表情很逗趣，這角度只有她撐得住。": "B", "C. 眼神依然有戲，透出清冷的氣質。": "C"}},
            {"q": "2. 輝人跟 Ggomo 的互動中，什麼畫面最深刻？", "options": {"A. 輝人跟 Ggomo 說話，牠卻不理她。": "A", "B. 兩者都散發「我行我素」的氛圍。": "B", "C. 抱著 Ggomo 時，溫柔帶點清傲的側臉.": "C"}},
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
            "C": {"type": "狐狸派：極致性感", "desc": "你完全沉溺於輝人的舞台魅力與成熟風情。在你身上散發出致命的優雅。"}
        }
    },
    "한국어": {
        "title": "【휘인 소울 시각 테스트】",
        "select_lang": "언어를 선택하세요",
        "restart_btn": "다시 하기",
        "questions": [
            {"q": "1. 휘인이 민낯으로 볼을 꼬집으며 찍은 셀카를 올렸을 때 반응은?", "options": {"A. 심쿵! 어쩜 이렇게 말랑콩떡 같지?": "A", "B. 표정이 너무 익살스럽네. 이런 각도는 휘인뿐.": "B", "C. 민낯인데도 눈빛이 깊네. 차갑고 몽환적이야.": "C"}},
            {"q": "2. 휘인과 꼬모(Ggomo)의 케미 중 가장 인상 깊은 장면은?", "options": {"A. 휘인이 말을 거는데 꼬모가 가볍게 무시하는 장면.": "A", "B. 둘 다 '마이웨이' 기질이 있어 닮아 보이는 분위기.": "B", "C. 꼬모를 안고 있을 때 비치는 다정하고 도도한 옆모습.": "C"}},
            {"q": "3. 무대 위에서 당신을 가장 사로잡는 휘인의 모습은?", "options": {"A. 무대 자체를 진심으로 즐기며 짓는 행복한 미소.": "A", "B. 예상치 못한 애드리브와 독보적인 스웨그.": "B", "C. 매혹적인 분위기와 무대를 압도하는 자신감.": "C"}},
            {"q": "4. 당신이 생각하는 휘인의 목소리 특징은?", "options": {"A. 오후의 햇살처럼 따스하고 치유해 주는 힘.": "A", "B. 스페셜티 커피처럼 층이 다양하고 오묘한 느낌.": "B", "C. 잘 숙성된 와인처럼 부드럽고 취하게 만드는 마력.": "C"}},
            {"q": "5. 예능에서 당신이 가장 좋아하는 휘인의 모습은?", "options": {"A. 보조개가 쏙 들어갈 정도로 호탕하게 웃는 모습.": "A", "B. 갑자기 튀어나오는 4차원적인 멘트나 엉뚱한 팩폭.": "B", "C. 혼란 속에서도 우아함을 유지하는 성숙한 모습.": "C"}},
            {"q": "6. 휘인의 패션 스타일 중 가장 잘 어울리는 것은?", "options": {"A. 오버사이즈 보이시 룩에 비니를 매치한 스타일.": "A", "B. 화려한 색감이나 독특한 스트릿 그래피티 룩.": "B", "C. 슬림한 핏의 셋업 수트로 완성한 신비로운 스타일.": "C"}},
            {"q": "7. 콘서트 앵콜곡으로 딱 한 곡만 고를 수 있다면?", "options": {"A. 〈Wheee〉": "A", "B. 〈EASY〉 (ft. Sik-K)": "B", "C. 〈Shhh〉": "C"}},
            {"q": "8. 휘인의 타투가 상징하는 것은 무엇이라고 생각하나요?", "options": {"A. 삶에 대한 순수한 애정과 자유를 향한 갈망.": "A", "B. 남다른 예술가적 영혼과 독특한 미학.": "B", "C. 성숙하고 신비로운, 서사가 담긴 여인의 향기.": "C"}},
            {"q": "9. 마마무 팀 내에서 휘인의 역할은 무엇인가요?", "options": {"A. 멤버들의 감정을 이어주는 따뜻한 힐링 아이콘.": "A", "B. 무대를 더 흥미롭게 만드는 영리한 천재 아티스트.": "B", "C. 소울풀한 감성과 섹시한 아우라를 더하는 핵심.": "C"}},
            {"q": "10. 휘인의 눈빛이 가장 자주 보내는 신호는?", "options": {"A. '우리 같이 놀자!'": "A", "B. '무슨 생각 해?'": "B", "C. '나만 바라봐.'": "C"}}
        ],
        "results": {
            "A": {"type": " 강아지파", "desc": "당신의 눈에 휘인은 '정석 귀요미' 그 자체입니다. 그녀의 미소와 보조개에 가장 쉽게 매료됩니다."},
            "B": {"type": " 고양이파", "desc": "당신은 휘인의 예술가적 기질을 가장 아낍니다. 당신 눈에 그녀는 고고하면서도 호기심 많은 고양이 같습니다."},
            "C": {"type": " 여우파", "desc": "당신은 휘인의 무대 위 아우라와 성숙한 분위기에 완전히 빠져 있습니다. 그녀는 우아함과 섹시함의 결정체입니다."}
        }
    },
    "English": {
        "title": "Whee In Soul Quiz",
        "select_lang": "Select Language",
        "restart_btn": "Restart",
        "questions": [
            {"q": "1. Whee In's bare-faced selfie pinching her cheeks, your reaction?", "options": {"A. AHH! So soft and squishy!": "A", "B. Hilarious; only she pulls off that angle.": "B", "C. Chic aura, her eyes tell a story.": "C"}},
            {"q": "2. Moment with Ggomo that impressed you most?", "options": {"A. Whee In talking while Ggomo ignores her.": "A", "B. Both giving off a 'doing my own thing' vibe.": "B", "C. Tender yet elegant pride when holding him.": "C"}},
            {"q": "3. What attracts you most during her stage performances?", "options": {"A. Genuine enjoyment and heartfelt smile.": "A", "B. Unique stage swagger and ad-libs.": "B", "C. 'Stage-master' confidence and allure.": "C"}},
            {"q": "4. How would you describe her voice quality?", "options": {"A. Afternoon sunshine—warm and healing.": "A", "B. Specialty coffee—complex and layered.": "B", "C. Aged red wine—silky and intoxicating.": "C"}},
            {"q": "5. What do you love most in her variety show footage?", "options": {"A. Uninhibited laughter with deep dimples.": "A", "B. Sudden quirky '4D' comments or roasts.": "B", "C. Staying elegant amidst the chaos.": "C"}},
            {"q": "6. Which fashion style does she pull off best?", "options": {"A. Oversized boyish hoodies and caps.": "A", "B. Bright colors and street-graffiti look.": "B", "C. Slim-fit blazers with mystery.": "C"}},
            {"q": "7. One song request at the end of a concert?", "options": {"A. 〈Wheee〉": "A", "B. 〈EASY〉 (ft. Sik-K)": "B", "C. 〈Shhh〉": "C"}},
            {"q": "8. What do you think her tattoos represent?", "options": {"A. Pure love for life and longing for freedom.": "A", "B. Unique artist soul and quirky aesthetics.": "B", "C. Maturity and mystery, a woman with a story.": "C"}},
            {"q": "9. Her role within MAMAMOO's group performances?", "options": {"A. The Sweetheart bridging emotions.": "A", "B. The Maverick bringing surprises.": "B", "C. The Soul adding jazz and sexy aura.": "C"}},
            {"q": "10. What message do her eyes usually send?", "options": {"A. 'Let's play!'": "A", "B. 'What are you thinking?'": "B", "C. 'Look at me.'": "C"}}
        ],
        "results": {
            "A": {"type": " Puppy Type", "desc": "In your eyes, Whee In is the definition of 'Standard Cuteness.'"},
            "B": {"type": " Cat Type", "desc": "You admire her artistic temperament and 'one-of-a-kind' soul."},
            "C": {"type": " Fox Type", "desc": "You're completely immersed in her stage presence and mature allure."}
        }
    }
}

# --- 4. CSS 樣式與狀態控制 ---

# 初始化狀態 (必須放在 CSS 設定之前，因為 CSS 需要判斷狀態)
if 'step' not in st.session_state: st.session_state.step = -2  # 從 -2 (封面背景頁) 開始
if 'answers' not in st.session_state: st.session_state.answers = []
if 'lang' not in st.session_state: st.session_state.lang = "繁體中文"
if 'recorded' not in st.session_state: st.session_state.recorded = False

# 讀取原本的背景圖
img_header = get_base64_file("Header.png")
img_middle = get_base64_file("Middle.png")
img_footer = get_base64_file("Footer.png")

# 讀取新的封面圖
img_start = get_base64_file("Start screen.png")

# 初始化動態 CSS 變數
bg_final = "none"
block_padding = "280px 20px 300px 20px !important" # 原本的 padding

# --- 核心邏輯修改：動態更換背景 ---
if st.session_state.step == -2:
    # 1. 封面頁狀態：使用 Start screen.png 作為唯一背景，並填滿
    if img_start:
        bg_start = f'url("data:image/png;base64,{img_start}")'
        # 強制背景置中、不重複、填滿區域 (cover)
        bg_final = f"{bg_start} center center / cover no-repeat !important"
    
    # 2. 封面頁狀態：調整 padding，讓 START 按鈕不要被 Header 擋住 (因為此時沒 Header)
    # 這裡的 padding-top 縮小，讓按鈕靠下浮現
    block_padding = "450px 20px 50px 20px !important" 

else:
    # 3. 正常測驗狀態：使用原本的紅底 + Header/Footer 三段式背景
    bg_header = f'url("data:image/png;base64,{img_header}")' if img_header else "none"
    bg_middle = f'url("data:image/png;base64,{img_middle}")' if img_middle else "none"
    bg_footer = f'url("data:image/png;base64,{img_footer}")' if img_footer else "none"
    
    # 原本的複雜背景設定
    bg_final = f"{bg_header}, {bg_footer}, {bg_middle} !important"

# --- 應用 CSS ---
st.markdown(f"""
    <style>
    header {{ visibility: hidden !important; height: 0px !important; }}
    
    /* 這裡應用動態計算出的背景 (bg_final) */
    .stApp {{ 
        background-color: #9d2933; /* 基礎紅底 */
        background-image: {bg_final};
        
        # 只有在非封面頁時，才應用原本的多重位置設定
        {"background-position: top center, bottom center, top center !important;" if st.session_state.step != -2 else ""}
        {"background-repeat: no-repeat, no-repeat, repeat-y !important;" if st.session_state.step != -2 else ""}
        
        background-size: min(100%, 420px) auto !important; 
    }}
    
    /* 這裡應用動態計算出的 Padding (block_padding) */
    .block-container {{
        max-width: 420px !important; 
        margin: auto; 
        padding: {block_padding}; 
    }}
    
    /* 以下樣式保持不變 */
    h1, h2, h3, h4 {{ color: #3d1b1b !important; text-align: center; }}
    
    .stMarkdown p {{
        background-color: rgba(255, 255, 255, 0.6);
        padding: 8px 15px !important; 
        border-radius: 10px; 
        color: #333333 !important;
    }}
    
    .stButton > button {{ 
        width: 100%; border-radius: 12px; background: white; color: #b71c1c; 
        font-weight: bold; border: 1.5px solid #b71c1c; margin-bottom: 5px;
        # 增加一點陰影，讓按鈕在背景上更明顯
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }}

    .result-box {{ 
        background: rgba(255,255,255,0.9); padding: 20px; border-radius: 20px; 
        text-align: center; color: black; border: 2px solid #b71c1c;
    }}
    .result-box h2 {{ 
        font-size: 1.6em; margin-top: 0px !important; margin-bottom: 5px !important; 
    }}
    .result-box p {{ 
        font-size: 0.95em; line-height: 1.6; margin-top: 0px !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. 背景音樂 (保持不變) ---
audio_base64 = get_base64_file("bgm.mp3")
if audio_base64:
    audio_html = f"""
        <div style="position: relative; z-index: 999; top: -150px; left: -10px; height: 0px;">
            <audio controls autoplay loop style="height: 35px; width: 44px; opacity: 0.85; border-radius: 50%; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.2));">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        </div>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 6. 流程控制 ---

# 重新取得當前語言資料 (防止 Restart 後出錯)
curr_data = LANG_MAP.get(st.session_state.lang, LANG_MAP["繁體中文"])

# 新增：封面啟動頁邏輯
if st.session_state.step == -2:
    # 這裡什麼都不用畫 (例如 st.image)，因為圖片已經在 CSS 的背景裡了。
    
    # 畫一個提示文字（可選，增加點擊感，背景半透明）
    st.markdown(f"""
        <div style="text-align: center; background-color: rgba(255,255,255,0.5); padding: 10px; border-radius: 10px; margin-bottom: 10px;">
            <span style="color: #3d1b1b; font-weight: bold;">2026 Whee In Birthday Event</span>
        </div>
    """, unsafe_allow_html=True)

    # 畫 START 按鈕
    if st.button("START / 進入測驗 / 시작하기", use_container_width=True):
        st.session_state.step = -1
        st.rerun()

# A. 語言選擇 (原有的邏輯，保持不變)
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

# B. 題目進行 (保持不變)
elif st.session_state.step < len(curr_data["questions"]):
    q_item = curr_data["questions"][st.session_state.step]
    st.write(f"**{q_item['q']}**")
    
    for text, val in q_item["options"].items():
        if st.button(text, key=f"btn_{st.session_state.step}_{val}"):
            st.session_state.answers.append(val)
            st.session_state.step += 1
            st.rerun()

# C. 結果顯示 (保持不變)
else:
    counts = Counter(st.session_state.answers)
    top_choice = counts.most_common(1)[0][0]
    res = curr_data["results"][top_choice]
    
    # 儲存結果
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
    
    st.write("") 
    if st.button(curr_data["restart_btn"], use_container_width=True):
        st.session_state.step = -1
        st.session_state.answers = []
        st.session_state.recorded = False
        st.rerun()
