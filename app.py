import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. 網站基礎設定 & 黑白型格設計 (Midnight Runners Vibe) ---
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

# --- 2. 連接 Google
