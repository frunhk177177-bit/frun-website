import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. 網站基礎設定 & CSS
# ==========================================
st.set_page_config(page_title="FRUN CLUB", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
    .stApp { background-color: #000000; }
    h1, h2, h3, .big-font { color: #FFFFFF !important; font-family: 'Oswald', sans-serif; text-transform: uppercase; }
    p, div, label, span, li, .small-font { color: #E0E0E0 !important; font-family: 'Helvetica', sans-serif; }
    .stTextInput > div > div > input { background-color: #121212; color: white; border: 1px solid #333; }
    .stButton > button { background-color: #FFFFFF; color: #000000 !important; font-family: 'Oswald', sans-serif; font-weight: bold; border: none; width: 100%; }
    .stButton > button:hover { background-color: #FF0055; color: #FFFFFF !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
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
# 4. 側邊選單 (Sidebar) - 含自動去小數點功能
# ==========================================
with st.sidebar:
    st.title("FRUN.")
    menu = st.radio("MENU", ["HOME", "EVENTS", "ADMIN"])
    st.markdown("---")
    
    if not st.session_state.user:
        st.caption("MEMBER ACCESS")
        
        login_name = st.text_input("USERNAME", key="login_name")
        login_pwd = st.text_input("PASSWORD", type="password", key="login_pwd")
        
        if st.button("LOGIN"):
            if login_name and login_pwd:
                try:
                    # 1. 讀取 Members 分頁
                    df_members = conn.read(worksheet="Members", ttl=0)
                    
                    # 2. 強力清洗資料 (這段是新的！)
                    # 把 Name 轉大寫
                    df_members['Name'] = df_members['Name'].astype(str).str.strip().str.upper()
                    
                    # === 關鍵修正：處理密碼 ===
                    # 先轉成字串，如果結尾是 .0 就把它切掉
                    df_members['Password'] = df_members['Password'].astype(str).str.strip()
                    df_members['Password'] = df_members['Password'].apply(lambda x: x.replace(".0", "") if x.endswith(".0") else x)
                    
                    # 使用者輸入也要清洗
                    clean_login_name = str(login_name).strip().upper()
                    clean_login_pwd = str(login_pwd).strip()
                    
                    # 3. 比對
                    user_found = df_members[
                        (df_members['Name'] == clean_login_name) & 
                        (df_members['Password'] == clean_login_pwd)
                    ]
                    
                    if not user_found.empty:
                        st.session_state.user = clean_login_name
                        st.success("WELCOME BACK.")
                        st.rerun()
                    else:
                        st.error("LOGIN FAILED")
                        # 簡單提示，不用顯示太多 Debug 資訊了
                        st.caption("請檢查帳號密碼是否正確。")
                            
                except Exception as e:
                    st.error(f"系統錯誤: {e}")
            else:
                st.warning("Enter Name & Password")
    else:
        st.write(f"⚡ HI, **{st.session_state.user}**")
        if st.button("LOGOUT"):
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

if menu == "HOME":
    st.title("FRUN - WE RUN FOR FUN")
    st.image("https://images.unsplash.com/photo-1552674605-469523170d9e?q=80&w=2070")
    st.info("📢 SYSTEM ONLINE.")

elif menu == "EVENTS":
    st.title("UPCOMING SESSIONS")
    st.markdown("_NO EXCUSES._")
    st.divider()
    if df.empty: st.warning("No events.")
    for index, row in df.iterrows():
        with st.container():
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {row['Event']}")
                st.markdown(f"**📍 {row['Location']}** | **🕒 {row['Date']} @ {row['Time']}**")
                if row['Description']: st.info(f"ℹ️ {row['Description']}")
                attendees_list = [x.strip() for x in str(row['Attendees']).split(",") if x.strip()]
                if attendees_list:
                    st.write(f"🔥 **{len(attendees_list)} RUNNERS IN:**")
                    st.markdown(" ".join([f"`{name}`" for name in attendees_list]), unsafe_allow_html=True)
            with c2:
                st.write("")
                st.write("")
                if st.session_state.user:
                    if st.session_state.user in attendees_list:
                        st.button("I'M IN ✓", key=f"btn_{index}", disabled=True)
                    else:
                        if st.button("JOIN +", key=f"btn_join_{index}"):
                            attendees_list.append(st.session_state.user)
                            df.at[index, "Attendees"] = ", ".join(attendees_list)
                            conn.update(worksheet="Sheet1", data=df)
                            st.toast("JOINED!")
                            st.rerun()
                else:
                    st.warning("LOGIN FIRST")
            st.markdown("---")

elif menu == "ADMIN":
    st.header("CREW CONTROL")
    if st.text_input("ADMIN PIN", type="password") == "8888":
        st.success("ACCESS GRANTED")
        with st.form("new_event"):
            e_name = st.text_input("Event Name")
            c1, c2 = st.columns(2)
            e_date = c1.text_input("Date")
            e_time = c2.text_input("Time")
            e_loc = st.text_input("Location")
            e_desc = st.text_area("Description")
            if st.form_submit_button("PUBLISH"):
                new_row = pd.DataFrame([{"Event": e_name, "Date": e_date, "Time": e_time, "Location": e_loc, "Description": e_desc, "Attendees": ""}])
                conn.update(worksheet="Sheet1", data=pd.concat([df, new_row], ignore_index=True))
                st.success("PUBLISHED")
                st.rerun()
