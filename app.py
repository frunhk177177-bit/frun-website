import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. 網站基礎設定 & 黑白風格 (CSS)
# ==========================================
st.set_page_config(page_title="FRUN CLUB", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
    
    /* 全站背景：深黑 */
    .stApp { background-color: #000000; }
    
    /* 字體設定 */
    h1, h2, h3, .big-font { 
        color: #FFFFFF !important; 
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    p, div, label, span, li, .small-font { 
        color: #E0E0E0 !important; 
        font-family: 'Helvetica', sans-serif; 
    }
    
    /* 輸入框與按鈕 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #121212; 
        color: white; 
        border: 1px solid #333;
    }
    .stButton > button {
        background-color: #FFFFFF;
        color: #000000 !important;
        border-radius: 0px;
        font-family: 'Oswald', sans-serif;
        font-weight: bold;
        text-transform: uppercase;
        border: none;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #FF0055; /* Neon Pink */
        color: #FFFFFF !important;
        box-shadow: 0 0 15px #FF0055;
    }
    
    /* 隱藏預設元素 */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 連接 Google Sheets 資料庫
# ==========================================
conn = st.connection("gsheets", type=GSheetsConnection)

# ==========================================
# 3. 初始化 Session State (使用者狀態)
# ==========================================
if 'user' not in st.session_state:
    st.session_state.user = None

# ==========================================
# 4. 側邊選單 (Sidebar) - 含會員登入邏輯
# ==========================================
with st.sidebar:
    st.title("FRUN.")
    menu = st.radio("MENU", ["HOME", "EVENTS", "ADMIN"])
    
    st.markdown("---")
    
    # === 會員登入區塊 ===
    if not st.session_state.user:
        st.caption("MEMBER ACCESS")
        
        # 輸入帳號密碼
        login_name = st.text_input("USERNAME", key="login_name")
        login_pwd = st.text_input("PASSWORD", type="password", key="login_pwd")
        
        if st.button("LOGIN"):
            if login_name and login_pwd:
                try:
                    # 讀取 'Members' 分頁
                    df_members = conn.read(worksheet="Members", ttl=0)
                    
                    # 比對帳號密碼 (轉大寫比對 Name, 密碼轉字串比對)
                    user_found = df_members[
                        (df_members['Name'].astype(str).str.upper() == login_name.upper()) & 
                        (df_members['Password'].astype(str) == login_pwd)
                    ]
                    
                    if not user_found.empty:
                        st.session_state.user = login_name.upper()
                        st.toast(f"WELCOME BACK, {st.session_state.user}")
                        st.rerun()
                    else:
                        st.error("WRONG NAME OR PASSWORD")
                except Exception as e:
                    st.error(f"登入失敗: 請檢查 Google Sheet 是否有 'Members' 分頁。")
            else:
                st.warning("Please enter name & password")
                
    else:
        # 登入成功後顯示
        st.write(f"⚡ HI, **{st.session_state.user}**")
        if st.button("LOGOUT"):
            st.session_state.user = None
            st.rerun()

# ==========================================
# 5. 主頁面邏輯
# ==========================================

# 先讀取活動資料 (Sheet1)
try:
    df = conn.read(worksheet="Sheet1", ttl=0)
    # 補全缺失欄位，防止報錯
    expected_cols = ["Event", "Date", "Time", "Location", "Description", "Attendees"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""
    df = df.fillna("")
except:
    # 如果讀取失敗，建立一個空的 DataFrame 防止網頁崩潰
    df = pd.DataFrame(columns=["Event", "Date", "Time", "Location", "Description", "Attendees"])

# === PAGE: HOME (首頁) ===
if menu == "HOME":
    st.title("RUN FAST. LIVE LOUD.")
    st.image("https://images.unsplash.com/photo-1552674605-469523170d9e?q=80&w=2070&auto=format&fit=crop")
    
    st.markdown("### LATEST NEWS")
    st.info("📢 SYSTEM ONLINE. MEMBER LOGIN REQUIRED FOR EVENTS.")

# === PAGE: EVENTS (活動頁) ===
elif menu == "EVENTS":
    st.title("UPCOMING SESSIONS")
    st.markdown("_NO EXCUSES._")
    st.divider()

    if df.empty:
        st.warning("No events found. Admin needs to add events.")

    # 顯示每個活動
    for index, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {row['Event']}")
                st.markdown(f"**📍 {row['Location']}** | **🕒 {row['Date']} @ {row['Time']}**")
                
                if row['Description']:
                    st.info(f"ℹ️ {row['Description']}")
                
                # 處理參加者名單
                attendees_str = str(row['Attendees'])
                attendees_list = [x.strip() for x in attendees_str.split(",") if x.strip()]
                
                if attendees_list:
                    st.write(f"🔥 **{len(attendees_list)} RUNNERS IN:**")
                    st.markdown(" ".join([f"`{name}`" for name in attendees_list]), unsafe_allow_html=True)
                else:
                    st.caption("Be the first to join.")

            with col2:
                st.write("") 
                st.write("") 
                
                if st.session_state.user:
                    # 檢查使用者是否已在名單內
                    if st.session_state.user in attendees_list:
                        st.button("I'M IN ✓", key=f"btn_done_{index}", disabled=True)
                    else:
                        if st.button("JOIN +", key=f"btn_join_{index}"):
                            # 加入名單邏輯
                            attendees_list.append(st.session_state.user)
                            new_attendees_str = ", ".join(attendees_list)
                            
                            # 更新資料庫
                            df.at[index, "Attendees"] = new_attendees_str
                            conn.update(worksheet="Sheet1", data=df)
                            
                            st.toast(f"BOOM! {st.session_state.user} JOINED.")
                            st.rerun()
                else:
                    st.warning("LOGIN FIRST")
            
            st.markdown("---")

# === PAGE: ADMIN (管理員後台) ===
elif menu == "ADMIN":
    st.header("CREW CONTROL")
    pwd = st.text_input("ADMIN PIN", type="password")
    
    if pwd == "8888": # 管理員密碼
        st.success("ACCESS GRANTED")
        
        with st.form("add_event"):
            st.subheader("CREATE NEW RUN")
            c1, c2 = st.columns(2)
            e_name = c1.text_input("Event Name")
            e_date = c2.text_input("Date")
            e_time = c1.text_input("Time")
            e_loc = c2.text_input("Location")
            e_desc = st.text_area("Description")
            
            if st.form_submit_button("PUBLISH"):
                # 建立新活動資料
                new_row = pd.DataFrame([{
                    "Event": e_name, 
                    "Date": e_date, 
                    "Time": e_time, 
                    "Location": e_loc, 
                    "Description": e_desc, 
                    "Attendees": ""
                }])
                
                # 合併並寫入 Google Sheets
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                
                st.success("EVENT PUBLISHED")
                st.rerun()

# === DEBUG 測試區 (請貼在 app.py 最下面) ===
st.divider()
st.subheader("🕵️‍♂️ DEBUG 模式：檢查會員名單")
try:
    # 嘗試讀取 Members 分頁
    df_debug = conn.read(worksheet="Members", ttl=0)
    st.write("✅ 成功讀取 Members 分頁！以下是電腦看到的資料：")
    st.dataframe(df_debug)
    
    st.write("👉 欄位名稱檢查：", df_debug.columns.tolist())
    
    # 檢查是否有 'Name' 和 'Password' 欄位
    if 'Name' not in df_debug.columns:
        st.error("❌ 找不到 'Name' 欄位！請檢查 Google Sheet A1 格子。")
    if 'Password' not in df_debug.columns:
        st.error("❌ 找不到 'Password' 欄位！請檢查 Google Sheet B1 格子。")
        
except Exception as e:
    st.error(f"❌ 讀取失敗：{e}")
    st.info("提示：這通常代表你的分頁名稱不叫 'Members'。")
