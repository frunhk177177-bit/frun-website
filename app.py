import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ---------------------------------------------------------
# 1. 網站基礎設定 & Midnight Runners 風格 CSS
# ---------------------------------------------------------
st.set_page_config(page_title="FRUN CLUB", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* 引入 Google Fonts: Oswald (粗體海報字) */
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
    
    /* 全站背景：深黑 */
    .stApp { background-color: #000000; }
    
    /* 標題與重點文字風格 */
    h1, h2, h3, .big-font { 
        color: #FFFFFF !important; 
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* 一般內文風格 */
    p, div, label, span, li, .small-font { 
        color: #E0E0E0 !important; 
        font-family: 'Helvetica', sans-serif; 
    }
    
    /* 輸入框與文字區域 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #121212; 
        color: white; 
        border: 1px solid #333;
    }
    
    /* 按鈕風格：型格直角 + 霓虹粉紅 Hover */
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
    
    /* 成功訊息樣式 */
    .stToast { background-color: #FF0055 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 連接 Google Sheets 資料庫 (含錯誤防護)
# ---------------------------------------------------------
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=0) # ttl=0 代表不快取，每次都抓最新資料
def load_data():
    try:
        # 嘗試讀取 Sheet1
        df = conn.read(worksheet="Sheet1")
        return df
    except Exception as e:
        return None

# 執行讀取
raw_df = load_data()

# 檢查資料是否讀取成功
if raw_df is None:
    st.error("⚠️ 資料庫連線失敗！請檢查：")
    st.info("1. Google Sheet 分頁名稱是否為 'Sheet1'？")
    st.info("2. Secrets 設定是否正確？")
    st.stop() # 停止執行，避免黑屏

# 資料清理 (確保欄位存在且無空值)
expected_cols = ["Event", "Date", "Time", "Location", "Description", "Attendees"]
df = raw_df.copy()
for col in expected_cols:
    if col not in df.columns:
        df[col] = "" # 若欄位缺失則補空字串
df = df.fillna("") # 將所有 NaN 轉為空字串

# ---------------------------------------------------------
# 3. 使用者登入狀態 (Session State)
# ---------------------------------------------------------
if 'user' not in st.session_state:
    st.session_state.user = None

# ---------------------------------------------------------
# 4. 側邊選單 (Sidebar)
# ---------------------------------------------------------
with st.sidebar:
    st.title("FRUN.")
    menu = st.radio("MENU", ["HOME", "EVENTS", "ADMIN"])
    
    st.markdown("---")
    
    # 簡易登入區
    if not st.session_state.user:
        st.caption("MEMBER ACCESS")
        name_input = st.text_input("ENTER NAME", key="login_input")
        if st.button("LOGIN"):
            if name_input:
                st.session_state.user = name_input.upper() # 轉大寫比較帥
                st.rerun()
    else:
        st.write(f"⚡ HI, **{st.session_state.user}**")
        if st.button("LOGOUT"):
            st.session_state.user = None
            st.rerun()

# ---------------------------------------------------------
# 5. 頁面邏輯
# ---------------------------------------------------------

# === HOME PAGE (首頁) ===
if menu == "HOME":
    st.title("RUN FAST. LIVE LOUD.")
    # 這裡放一張很有 VIBE 的跑者圖片
    st.image("https://images.unsplash.com/photo-1552674605-469523170d9e?q=80&w=2070&auto=format&fit=crop")
    
    st.markdown("### LATEST NEWS")
    st.info("📢 SYSTEM ONLINE. READY TO RUN.")

# === EVENTS PAGE (活動頁 - 核心功能) ===
elif menu == "EVENTS":
    st.title("UPCOMING SESSIONS")
    st.markdown("_NO EXCUSES._")
    st.divider()

    # 檢查是否有活動
    if df.empty:
        st.warning("No events scheduled yet.")
    
    # 顯示活動列表
    for index, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            # --- 左側：活動資訊 ---
            with col1:
                st.markdown(f"### {row['Event']}")
                st.markdown(f"**📍 {row['Location']}** | **🕒 {row['Date']} @ {row['Time']}**")
                
                # 顯示 Admin 填寫的描述
                if row['Description']:
                    st.info(f"ℹ️ {row['Description']}")
                
                # 處理參加者名單 (字串轉清單)
                attendees_str = str(row['Attendees'])
                # 將 "Alex, Sarah" 切割成 ["Alex", "Sarah"]
                attendees_list = [x.strip() for x in attendees_str.split(",") if x.strip()]
                
                if attendees_list:
                    st.write(f"🔥 **{len(attendees_list)} RUNNERS IN:**")
                    # 用 Badge 風格顯示名字
                    st.markdown(" ".join([f"`{name}`" for name in attendees_list]), unsafe_allow_html=True)
                else:
                    st.caption("Be the first to join.")

            # --- 右側：報名按鈕 ---
            with col2:
                st.write("") # 佔位
                st.write("") 
                
                if st.session_state.user:
                    # 檢查是否已報名
                    if st.session_state.user in attendees_list:
                        st.button("I'M IN ✓", key=f"btn_done_{index}", disabled=True)
                    else:
                        # === 關鍵：寫入 Google Sheets ===
                        if st.button("JOIN +", key=f"btn_join_{index}"):
                            # 1. 把新名字加到清單
                            attendees_list.append(st.session_state.user)
                            # 2. 轉回字串格式 (例如 "Alex, Sarah, Jason")
                            new_attendees_str = ", ".join(attendees_list)
                            # 3. 更新 DataFrame 中的那一格
                            df.at[index, "Attendees"] = new_attendees_str
                            # 4. 寫回 Google Sheets
                            try:
                                conn.update(worksheet="Sheet1", data=df)
                                st.toast(f"BOOM! {st.session_state.user} JOINED THE CREW.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"寫入失敗: {e}")
                else:
                    st.warning("LOGIN FIRST")
            
            st.markdown("---")

# === ADMIN PAGE (管理員頁面) ===
elif menu == "ADMIN":
    st.header("CREW CONTROL")
    pwd = st.text_input("ADMIN PIN", type="password")
    
    if pwd == "8888": # 管理員密碼
        st.success("ACCESS GRANTED")
        
        with st.form("add_event_form"):
            st.subheader("CREATE NEW RUN")
            c1, c2 = st.columns(2)
            e_name = c1.text_input("Event Name")
            e_date = c2.text_input("Date (e.g. Feb 20)")
            e_time = c1.text_input("Time (e.g. 19:30)")
            e_loc = c2.text_input("Location")
            
            # Admin 專屬描述欄位
            e_desc = st.text_area("Description / Details", placeholder="Example: 5K Easy run with music.")
            
            if st.form_submit_button("PUBLISH EVENT"):
                # 建立新的一行資料
                new_row = pd.DataFrame([{
                    "Event": e_name,
                    "Date": e_date,
                    "Time": e_time,
                    "Location": e_loc,
                    "Description": e_desc,
                    "Attendees": "" # 新活動預設沒人
                }])
                
                # 合併並寫入
                updated_df = pd.concat([df, new_row], ignore_index=True)
                try:
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.success("EVENT LIVE! CHECK THE DATABASE.")
                    st.rerun()
                except Exception as e:
                    st.error(f"發布失敗: {e}")
