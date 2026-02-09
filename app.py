import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. 網站基礎設定 & 野獸派工業風格 (Brutalist CSS)
# ==========================================
st.set_page_config(page_title="FRUN CLUB", page_icon="BLK", layout="centered")

st.markdown("""
    <style>
    /* 引入字體：Oswald (標題), JetBrains Mono (數據) */
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* 全站背景：純黑 */
    .stApp { background-color: #000000; }
    
    /* 標題設定：巨大、粗體、全大寫 */
    h1, h2, h3 { 
        color: #FFFFFF !important; 
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 2px;
    }
    
    /* 內文設定：等寬字體，像終端機一樣 */
    p, div, label, span, li, input, textarea { 
        color: #B0B0B0 !important; 
        font-family: 'JetBrains Mono', monospace !important; 
        font-size: 14px;
    }
    
    /* 輸入框：極簡線條 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #000000; 
        color: white; 
        border: 1px solid #333;
        border-radius: 0px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FFFFFF;
    }
    
    /* 按鈕：實心白塊，黑字，無圓角 */
    .stButton > button {
        background-color: #FFFFFF;
        color: #000000 !important;
        border-radius: 0px;
        font-family: 'Oswald', sans-serif;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid #FFFFFF;
        width: 100%;
        padding: 12px 0;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #000000;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF;
    }
    
    /* 隱藏多餘元素 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    /* 分隔線樣式 */
    hr { margin: 2em 0; border-color: #333; }
    
    /* 參加者標籤 */
    .attendee-tag {
        border: 1px solid #444;
        padding: 2px 8px;
        font-size: 12px;
        margin-right: 6px;
        color: #888;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 連接 Google Sheets
# ==========================================
conn = st.connection("gsheets", type=GSheetsConnection)

# ==========================================
# 3. Session State
# ==========================================
if 'user' not in st.session_state:
    st.session_state.user = None

# ==========================================
# 4. 側邊選單 (Sidebar)
# ==========================================
with st.sidebar:
    st.title("FRUN.")
    st.markdown("---")
    menu = st.radio("NAVIGATION", ["HOME", "EVENTS", "ADMIN"])
    st.markdown("---")
    
    if not st.session_state.user:
        st.caption("/// MEMBER ACCESS")
        
        login_name = st.text_input("USERNAME", key="login_name")
        login_pwd = st.text_input("PASSWORD", type="password", key="login_pwd")
        
        if st.button("ENTER SYSTEM"):
            if login_name and login_pwd:
                try:
                    df_members = conn.read(worksheet="Members", ttl=0)
                    
                    # 資料清洗
                    df_members['Name'] = df_members['Name'].astype(str).str.strip().str.upper()
                    df_members['Password'] = df_members['Password'].astype(str).str.strip()
                    df_members['Password'] = df_members['Password'].apply(lambda x: x.replace(".0", "") if x.endswith(".0") else x)
                    
                    clean_name = str(login_name).strip().upper()
                    clean_pwd = str(login_pwd).strip()
                    
                    user_found = df_members[
                        (df_members['Name'] == clean_name) & 
                        (df_members['Password'] == clean_pwd)
                    ]
                    
                    if not user_found.empty:
                        st.session_state.user = clean_name
                        st.toast(f"ACCESS GRANTED: {clean_name}")
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED")
                except Exception as e:
                    st.error("DB CONNECTION ERROR")
    else:
        st.write(f"OPERATOR: {st.session_state.user}")
        if st.button("DISCONNECT"):
            st.session_state.user = None
            st.rerun()

# ==========================================
# 5. 主頁面內容
# ==========================================
try:
    df = conn.read(worksheet="Sheet1", ttl=0)
    for col in ["Event", "Date", "Time", "Location", "Description", "Attendees"]:
        if col not in df.columns: df[col] = ""
    df = df.fillna("")
except:
    df = pd.DataFrame()

# === PAGE: HOME ===
if menu == "HOME":
    st.title("RUN FAST.\nLIVE LOUD.") # 換行顯示更有張力
    st.image("https://images.unsplash.com/photo-1552674605-469523170d9e?q=80&w=2070", use_column_width=True)
    
    st.markdown("---")
    st.markdown("### SYSTEM STATUS")
    st.text("ONLINE // ALL SYSTEMS GO")
    st.text("NEXT SESSION: CHECK EVENTS TAB")

# === PAGE: EVENTS ===
elif menu == "EVENTS":
    st.title("SCHEDULE")
    st.markdown("---")

    if df.empty: st.text("NO UPCOMING SESSIONS.")

    # 顯示活動 (倒序，最新的在上面)
    for index, row in df.iterrows():
        with st.container():
            # 使用兩欄佈局：左邊資訊，右邊按鈕
            c1, c2 = st.columns([0.7, 0.3])
            
            with c1:
                st.markdown(f"## {row['Event']}")
                
                # 使用純文字標籤設計
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <span style="color: #666;">[DATE]</span> {row['Date']}<br>
                    <span style="color: #666;">[TIME]</span> {row['Time']}<br>
                    <span style="color: #666;">[LOC ]</span> {row['Location']}
                </div>
                """, unsafe_allow_html=True)
                
                if row['Description']:
                    st.markdown(f"""
                    <div style="border-left: 2px solid #333; padding-left: 10px; margin: 10px 0; color: #888;">
                        {row['Description']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # 參加者名單
                attendees_list = [x.strip() for x in str(row['Attendees']).split(",") if x.strip()]
                if attendees_list:
                    st.markdown(f"<div style='margin-top:10px; font-size:12px; color:#555;'>CONFIRMED ({len(attendees_list)}):</div>", unsafe_allow_html=True)
                    # 顯示名單
                    names_html = "".join([f"<span class='attendee-tag'>{name}</span>" for name in attendees_list])
                    st.markdown(names_html, unsafe_allow_html=True)
                else:
                    st.text("WAITING FOR RUNNERS...")

            with c2:
                st.write("") 
                if st.session_state.user:
                    if st.session_state.user in attendees_list:
                        st.button("CONFIRMED", key=f"btn_{index}", disabled=True)
                    else:
                        if st.button("RSVP", key=f"btn_join_{index}"):
                            attendees_list.append(st.session_state.user)
                            df.at[index, "Attendees"] = ", ".join(attendees_list)
                            conn.update(worksheet="Sheet1", data=df)
                            st.rerun()
                else:
                    st.markdown("<div style='text-align:center; padding:10px; border:1px solid #333; font-size:12px;'>LOGIN REQ.</div>", unsafe_allow_html=True)
            
            st.markdown("---") # 分隔線

# === PAGE: ADMIN ===
elif menu == "ADMIN":
    st.header("CONTROL PANEL")
    if st.text_input("ACCESS PIN", type="password") == "8888":
        st.success("AUTHORIZED")
        st.markdown("---")
        with st.form("new_event"):
            st.subheader("NEW ENTRY")
            e_name = st.text_input("EVENT NAME")
            c1, c2 = st.columns(2)
            e_date = c1.text_input("DATE (YYYY-MM-DD)")
            e_time = c2.text_input("TIME (HH:MM)")
            e_loc = st.text_input("LOCATION")
            e_desc = st.text_area("DETAILS / NOTES")
            
            if st.form_submit_button("PUBLISH"):
                new_row = pd.DataFrame([{"Event": e_name, "Date": e_date, "Time": e_time, "Location": e_loc, "Description": e_desc, "Attendees": ""}])
                conn.update(worksheet="Sheet1", data=pd.concat([df, new_row], ignore_index=True))
                st.rerun()
