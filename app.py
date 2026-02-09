# ---------------------------------------------------------
# 4. 側邊選單 (Sidebar) - 升級版登入系統
# ---------------------------------------------------------
with st.sidebar:
    st.title("FRUN.")
    menu = st.radio("MENU", ["HOME", "EVENTS", "ADMIN"])
    
    st.markdown("---")
    
    # === 真．會員登入系統 ===
    if not st.session_state.user:
        st.caption("MEMBER ACCESS")
        
        # 1. 輸入帳號密碼
        login_name = st.text_input("USERNAME", key="login_name")
        login_pwd = st.text_input("PASSWORD", type="password", key="login_pwd")
        
        if st.button("LOGIN"):
            if login_name and login_pwd:
                try:
                    # 2. 去 Google Sheet 抓取 'Members' 分頁
                    df_members = conn.read(worksheet="Members", ttl=0)
                    
                    # 3. 比對帳號 (不分大小寫)
                    # 這裡做一個篩選：找名字一樣，且密碼一樣的那一行
                    user_found = df_members[
                        (df_members['Name'].astype(str).str.upper() == login_name.upper()) & 
                        (df_members['Password'].astype(str) == login_pwd)
                    ]
                    
                    if not user_found.empty:
                        # 4. 登入成功
                        st.session_state.user = login_name.upper()
                        st.success("WELCOME BACK.")
                        st.rerun()
                    else:
                        # 5. 登入失敗
                        st.error("WRONG NAME OR PASSWORD")
                except Exception as e:
                    st.error(f"系統錯誤: 找不到 Members 分頁? {e}")
            else:
                st.warning("Please enter name & password")
                
    else:
        # 登入後的畫面
        st.write(f"⚡ HI, **{st.session_state.user}**")
        if st.button("LOGOUT"):
            st.session_state.user = None
            st.rerun()
