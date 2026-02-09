import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 網站基礎設定 & 黑白型格設計 ---
st.set_page_config(page_title="FRUN CLUB", page_icon="⚫", layout="centered")

st.markdown("""
    <style>
    /* 全站黑底白字 */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* 字體設定 */
    h1, h2, h3, p, div, label, span, li { 
        color: #FFFFFF !important; 
        font-family: 'Helvetica Now', 'Helvetica', sans-serif; 
    }
    
    /* 隱藏預設選單 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* 按鈕樣式 (Sporty Block) */
    .stButton > button {
        background-color: #FFFFFF;
        color: #000000 !important;
        border-radius: 0px;
        font-weight: 800;
        text-transform: uppercase;
        border: 1px solid white;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #000000;
        color: #FFFFFF !important;
        border: 1px solid white;
    }

    /* 報名名單的樣式 */
    .attendee-tag {
        background-color: #222;
        padding: 2px 8px;
        margin-right: 5px;
        font-size: 0.8em;
        border: 1px solid #444;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 初始化資料 (加入 'Attendees' 名單) ---
if 'events' not in st.session_state:
    st.session_state.events = [
        {
            "id": 1, 
            "Event": "URBAN NIGHT 5K", 
            "Date": "FEB 14 (WED)", 
            "Time": "20:00", 
            "Loc": "Central Pier 10", 
            "Attendees": ["Alex", "Sarah", "J-Dawg"] # 預設假名單
        },
        {
            "id": 2, 
            "Event": "SUNDAY LSD 15K", 
            "Date": "FEB 18 (SUN)", 
            "Time": "07:00", 
            "Loc": "Repulse Bay", 
            "Attendees": ["Coach K", "Sam"] 
        },
    ]

# 模擬登入狀態
if 'user' not in st.session_state:
    st.session_state.user = None

# --- 3. 側邊選單 ---
with st.sidebar:
    st.title("FRUN.")
    menu = st.radio("MENU", ["HOME", "EVENTS", "LOGIN"])
    st.markdown("---")
    if st.session_state.user:
        st.write(f"👤 LOGGED IN AS: **{st.session_state.user}**")
        if st.button("LOGOUT"):
            st.session_state.user = None
            st.rerun()

# --- 4. 頁面邏輯 ---

# === LOGIN PAGE ===
if menu == "LOGIN":
    st.header("MEMBER ACCESS")
    
    if not st.session_state.user:
        name_input = st.text_input("ENTER YOUR NAME TO JOIN")
        if st.button("ENTER SYSTEM"):
            if name_input:
                st.session_state.user = name_input.upper() # 自動變大寫，比較型
                st.success(f"WELCOME, {name_input.upper()}")
                st.rerun()
    else:
        st.success("YOU ARE ALREADY LOGGED IN.")
        st.info("Go to 'EVENTS' to join the runs.")

# === EVENTS PAGE (核心功能) ===
elif menu == "EVENTS":
    st.title("UPCOMING SESSIONS")
    st.markdown("Join the crew. No excuses.")
    st.divider()

    for i, event in enumerate(st.session_state.events):
        # 顯示活動卡片
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(event['Event'])
                st.caption(f"📍 {event['Loc']} | 🕒 {event['Date']} @ {event['Time']}")
                
                # --- 這裡就是你要的功能：顯示誰參加了 ---
                attendee_list = event['Attendees']
                count = len(attendee_list)
                
                if count > 0:
                    st.markdown(f"**🔥 {count} PEOPLE JOINED:**")
                    # 將名單變成字串顯示
                    names_display = ", ".join(attendee_list)
                    st.markdown(f"<span style='color:#888'>{names_display}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("*Be the first to join.*")

            with col2:
                # 只有登入後才能按按鈕
                if st.session_state.user:
                    # 檢查使用者是否已經在名單內
                    if st.session_state.user in event['Attendees']:
                        st.button("I'M IN ✓", key=f"joined_{i}", disabled=True)
                    else:
                        if st.button("JOIN +", key=f"join_{i}"):
                            # 將使用者加入名單
                            event['Attendees'].append(st.session_state.user)
                            st.toast(f"BOOM! You're in for {event['Event']}!")
                            st.rerun()
                else:
                    st.caption("Login to RSVP")
            
            st.divider()

# === HOME PAGE ===
elif menu == "HOME":
    st.title("RUN FAST. LIVE LOUD.")
    # 這裡可以放一張很酷的跑步背景圖
    st.image("https://images.unsplash.com/photo-1552674605-469523170d9e?q=80&w=2070&auto=format&fit=crop", use_column_width=True)
    
    st.markdown("### LATEST NEWS")
    st.info("📢 NEW DROP: FRUN Black Series Tee available next week.")
