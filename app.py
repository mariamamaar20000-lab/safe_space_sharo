import streamlit as st
import google.generativeai as genai
import time

# 1. الربط بالمفتاح الجديد
API_KEY = "AIzaSyBN23Iip1T1gcTNhrNHerkWZYcDPwAzsLM"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# تنسيق العيادة
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; direction: rtl; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #38bdf8; text-align: right; }
    .title { color: #38bdf8; text-align: center; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 عيادة دكتور شارون</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    role_class = "د. شارون" if msg["role"] == "assistant" else "أنت"
    st.markdown(f'<div class="chat-bubble"><b>{role_class}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# منطقة الكلام
user_input = st.chat_input("احكي، أنا سامعك...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر..."):
        # نظام المحاولات (Retry Logic)
        success = False
        retries = 0
        while not success and retries < 3: # هيحاول 3 مرات لو السيرفر مضغوط
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = (
                    "أنت دكتور شارون، معالج نفسي مصري حكيم. "
                    "تحدث بالعامية المصرية الراقية فقط. خليك إنساني وودود جداً. "
                    "المريض بيقولك: " + user_input
                )
                response = model.generate_content(prompt)
                reply = response.text
                
                st.session_state.messages.append({"role": "assistant", "content": reply})
                success = True
                st.rerun()
            except Exception as e:
                retries += 1
                time.sleep(1) # بيستنى ثانية قبل ما يحاول تاني
        
        if not success:
            st.warning("العيادة زحمة جداً دلوقتي يا بطل، خد نَفَس وكرر كلامك كمان لحظة وهرد عليك!")

if st.button("🗑️ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
