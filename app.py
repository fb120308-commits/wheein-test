import streamlit as st
import base64
from collections import Counter

# --- 1. 圖片處理函數 ---
def get_base64_image(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: 
        return None

# --- 2. 測驗資料內容 (包含中、韓、英三語系) ---
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
            "A": {"type": " 狗派：可愛元氣", "desc": "在你眼裡，輝人就是那個「定式可愛」的代表。你最容易被她的笑容、酒窩和親和力擊倒。對你來說，她是一個溫暖、真誠的元氣少女，只要她笑，世界就亮了。"},
            "B": {"type": " 貓派：古靈精怪", "desc": "你最欣賞輝人的藝術家氣質。在她身上你看到高傲卻好奇的靈魂。你著迷於她的神祕與冷靜，即使她「營業不積極」，你也覺得這才是她最迷人的地方。"},
            "C": {"type": " 狐狸派：極致性感", "desc": "你完全沉溺於輝人的舞台魅力與成熟風情。在你眼裡，她是優雅與性感的化身，眼神與撥髮動作都散發致命誘惑力。她是個讓人想不斷接近的神祕存在。"}
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
            "A": {"type": " 강아지파", "desc": "당신의 눈에 휘인은 '정석 귀요미' 그 자체입니다. 그녀의 미소와 보조개에 가장 쉽게 매료됩니다. 당신에게 휘인은 따뜻하고 에너지 넘치는 소녀로, 그녀가 웃으면 세상이 환해진다고 느낍니다."},
            "B": {"type": " 고양이파", "desc": "당신은 휘인의 예술가적 기질을 가장 아낍니다. 당신 눈에 그녀는 고고하면서도 호기심 많은 고양이 같습니다. 독특한 취향을 가진 그녀의 신비로움과 무심함조차 가장 큰 매력이라고 생각합니다."},
            "C": {"type": " 여우파", "desc": "당신은 휘인의 무대 위 아우라와 성숙한 분위기에 완전히 빠져 있습니다. 그녀는 우아함과 섹시함의 결정체입니다. 눈빛 하나에도 치명적인 유혹이 서려 있으며, 깊이를 알 수 없는 신비로운 존재입니다."}
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
            "A": {"type": " Puppy Type", "desc": "In your eyes, Whee In is the definition of 'Standard Cuteness.' You're easily defeated by her smile and dimples."},
            "B": {"type": " Cat Type", "desc": "You admire her artistic temperament and 'one-of-a-kind' soul. To you, she's like a proud yet curious cat."},
            "C": {"type": " Fox Type", "desc": "You're completely immersed in her stage presence and mature allure. In your eyes, she is the incarnation of elegance."}
        }
    }
}

# --- 3. CSS 樣式設定 (雙括號完全防錯版) ---
img_data = get_base64_image("Whee In The Test.png")
bg_css = f'url("data:image/png;base64,{img_data}")' if img_data else "none"

st.markdown(f"""
   <style>
    /* 【關鍵修正 1】徹底隱藏 Streamlit 預設的頂部選單，不讓它擋住標題！ */
    header {{ visibility: hidden !important; height: 0px !important; }}
    
    .stApp {{ background-color: #9d2933; }}
    
    .block-container {{
        background-image: {bg_css};
        /* 【關鍵修正 2】寬度 100% 貼齊螢幕，高度按原圖比例縮放，保證不變形不裁切！ */
        background-size: 100% auto !important; 
        background-position: top center !important; 
        background-repeat: no-repeat !important;
        
        max-width: 420px !important; 
        min-height: 100vh !important;
        
        margin: auto; 
        /* 稍微把左右 padding 縮小，讓手機版按鈕不會太擠 */
        padding: 260px 20px 50px 20px !important; 
    }}
    
    /* 這裡只針對文字加底色，沒有幽靈透明框了 */
    .stMarkdown {{
        background-color: rgba(255, 255, 255, 0.5);
        padding: 5px 15px; 
        border-radius: 10px; 
    }}
    
    .stButton > button {{ 
        width: 100%; border-radius: 15px; background: white; 
        color: #b71c1c; font-weight: bold; border: 1.5px solid #b71c1c;
    }}
    
    /* 結果呈現框 (所有括號都已使用雙括號防錯) */
    .result-box {{ 
        background: rgba(255,255,255,0.9); padding: 20px; 
        border-radius: 20px; text-align: center; color: black; border: 2px solid #b71c1c;
    }}
    
    .result-box h1 {{
        font-size: 1.8em; 
        margin-bottom: 10px;
    }}
    
    .result-box p {{
        font-size: 0.95em; 
        line-height: 1.6;  
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 流程控制 ---
if 'step' not in st.session_state: st.session_state.step = -1
if 'answers' not in st.session_state: st.session_state.answers = []
if 'lang' not in st.session_state: st.session_state.lang = "繁體中文"

# 根據選擇的語言載入資料
curr_data = LANG_MAP.get(st.session_state.lang, LANG_MAP["繁體中文"])

# A. 語言選擇畫面
if st.session_state.step == -1:
    st.markdown("<h3 style='text-align:center;'>Select Language</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    # 使用按鈕選擇語言並更新狀態
    if col1.button("繁體中文", use_container_width=True):
        st.session_state.lang = "繁體中文"
        st.session_state.step = 0
        st.rerun()
    if col2.button("한국어", use_container_width=True):
        st.session_state.lang = "한국어"
        st.session_state.step = 0
        st.rerun()
    if col3.button("English", use_container_width=True):
        st.session_state.lang = "English"
        st.session_state.step = 0
        st.rerun()

# B. 題目進行畫面
elif st.session_state.step < len(curr_data["questions"]):
    q_idx = st.session_state.step
    q_item = curr_data["questions"][q_idx]
    st.progress((q_idx + 1) / len(curr_data["questions"]))
    st.write(f"**{q_item['q']}**")
    for text, val in q_item["options"].items():
        if st.button(text, key=f"q_{q_idx}_{val}"):
            st.session_state.answers.append(val)
            st.session_state.step += 1
            st.rerun()

# C. 結果顯示畫面
else:
    counts = Counter(st.session_state.answers)
    top_choice = counts.most_common(1)[0][0]
    res = curr_data["results"][top_choice]
    
    st.balloons()
    st.markdown(f"""
        <div class='result-box'>
            <h1>{res['type']}</h1>
            <p>{res['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    
    # 將重新測驗按鈕置中
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button(curr_data["restart_btn"], use_container_width=True):
            st.session_state.step = -1
            st.session_state.answers = []
            st.rerun()
