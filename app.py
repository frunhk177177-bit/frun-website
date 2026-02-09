import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 設定 & Midnight Runners 風格 CSS ---
st.set_page_config(page_title="FRUN CLUB", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* 引入 Google Fonts: Oswald (粗體海報字) */
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');

    /* 全站背景：深黑 */
    .stApp { background-color: #000000; }
    
    /* 標題風格 - 模仿 Midnight Runners 的大字 */
    h1, h2, h3 { 
        color: #FFFFFF !important; 
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* 內文風格 */
    p, div, label, span, li { 
        color: #E0E0E0 !important; 
        font-family: 'Helvetica', sans-serif; 
    }
    
    /* 隱藏預設元素 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* 輸入框：深灰底白字 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #121212; 
        color: white; 
        border: 1px solid #333;
        border-radius: 0px;
    }

    /* 按鈕：Midnight Runners 風格 (霓虹粉紅 Hover 效果) */
    .stButton > button {
        background-color: #FFFFFF;
        color: #000000 !important;
        border-radius: 0px; /* 直角 */
        font-family: 'Oswald', sans-serif;
        font-size: 18px;
        font-weight: bold;
        text-transform: uppercase;
        border: none;
        transition: all 0.2s ease;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #FF0055; /* Neon Pink */
        color: #FFFFFF !important;
        box-shadow: 0 0 10px #FF0055; /* 發光效果 */
    }

    /* 活動卡片外框 */
    .event-card {
        border: 1px solid #333;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #0a0a0a;
    }
    
    /* 參加者標籤 */
    .attendee-badge {
        background-color: #FF0055;
        color: white;
        padding: 2px 6px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 4px;
        border-radius: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 初始化資料 (加入 'Description' 欄位) ---
if 'events' not in st.session_state:
    st.session_state.events = [
        {
            "id": 1, 
            "Event": "NEON NIGHT RUN 10K", 
            "Date": "FEB 14 (WED)", 
            "Time": "19:30", 
            "Loc": "Central Harbourfront", 
            "Desc": "Music synced run. 3 workout stations (Burpees, Squats). Bring the energy!",
            "Attendees": ["ALEX", "SARAH", "MIKE"]
        },
        {
            "id": 2, 
            "Event": "SUNDAY RECOVERY", 
            "Date": "FEB 18 (SUN)", 
            "Time": "08:00", 
            "Loc": "The Peak", 
            "Desc": "Easy pace. Coffee afterwards. No music, just vibes.",
            "Attendees": ["COACH K"] 
        },
    ]

# 模擬使用者狀態
if 'user' not in st.session_state:
    st.session_state.user = None

# --- 3. 側邊選單 ---
with st.sidebar:
    st.title("FRUN.")
    menu = st.radio("MENU", ["HOME", "EVENTS", "ADMIN"])
    
    st.markdown("---")
    # 簡易登入區塊 (放在 Sidebar 比較不佔空間)
    if not st.session_state.user:
        st.caption("MEMBER LOGIN")
        name_input = st.text_input("YOUR NAME", key="login_input")
        if st.button("ENTER"):
            if name_input:
                st.session_state.user = name_input.upper()
                st.rerun()
    else:
        st.write(f"⚡ WELCOME, **{st.session_state.user}**")
        if st.button("LOGOUT"):
            st.session_state.user = None
            st.rerun()

# --- 4. 頁面邏輯 ---

# === HOME PAGE ===
if menu == "HOME":
    st.title("OUR CITY. OUR RUN.")
    st.markdown("### WE RUN LOUD.")
    
    # 這裡放一張很有 Midnight Runners 感覺的照片 (Unsplash)
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070&auto=format&fit=crop", use_column_width=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.header("NEXT EVENT")
        next_event = st.session_state.events[0]
        st.markdown(f"**{next_event['Event']}**")
        st.caption(f"{next_event['Date']} | {next_event['Loc']}")
    with col2:
        st.header("THE CREW")
        st.markdown("Join a community of runners who refuse to be average.")

# === EVENTS PAGE (核心功能) ===
elif menu == "EVENTS":
    st.title("UPCOMING SESSIONS")
    st.markdown("_MUSIC. SWEAT. VIBES._")
    st.divider()

    for i, event in enumerate(st.session_state.events):
        # 這裡用 st.container 模擬卡片
        with st.container():
            # 上半部：標題與時間
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {event['Event']}") 
                st.markdown(f"**📍 {event['Loc']}** |  **🕒 {event['Date']} @ {event['Time']}**")
                
                # --- 新增功能：顯示 Description ---
                if event['Desc']:
                    st.info(f"ℹ️ {event['Desc']}")
                
                # --- 顯示已報名的人 (Social Proof) ---
                attendees = event['Attendees']
                if attendees:
                    st.write(f"🔥 **{len(attendees)} RUNNERS IN:**")
                    # 用 Badge 風格顯示名字
                    st.markdown(" ".join([f"`{name}`" for name in attendees]), unsafe_allow_html=True)
                else:
                    st.caption("Be the first to join.")

            with c2:
                st.write("") #用來佔位對齊
                st.write("") 
                if st.session_state.user:
                    if st.session_state.user in event['Attendees']:
                        st.success("YOU'RE IN ✓")
                    else:
                        if st.button("JOIN PARTY", key=f"join_{i}"):
                            event['Attendees'].append(st.session_state.user)
                            st.toast("BOOM! LIST UPDATED.")
                            st.rerun()
                else:
                    st.warning("LOGIN TO JOIN")
            
            st.markdown("---")

# === ADMIN PAGE (管理員) ===
elif menu == "ADMIN":
    st.header("CREW CONTROL")
    pwd = st.text_input("ADMIN PIN", type="password")
    
    if pwd == "8888":
        st.success("ACCESS GRANTED")
        
        with st.form("create_event"):
            st.subheader("CREATE NEW RUN")
            
            # 必填欄位
            col_a, col_b = st.columns(2)
            with col_a:
                e_name = st.text_input("Event Name (e.g. NEON 10K)")
                e_date = st.text_input("Date (e.g. FEB 20)")
            with col_b:
                e_time = st.text_input("Time (e.g. 19:30)")
                e_loc = st.text_input("Location")
            
            # --- 新增功能：活動詳細內容 ---
            e_desc = st.text_area("Description / Workout Details", 
                                  placeholder="Describe the vibe, the music, or the workout plan...")
            
            submitted = st.form_submit_button("PUBLISH EVENT")
            
            if submitted:
                new_event = {
                    "id": len(st.session_state.events) + 1,
                    "Event": e_name,
                    "Date": e_date,
                    "Time": e_time,
                    "Loc": e_loc,
                    "Desc": e_desc, # 儲存描述
                    "Attendees": []
                }
                st.session_state.events.append(new_event)
                st.success("EVENT LIVE! CHECK THE 'EVENTS' TAB.")
