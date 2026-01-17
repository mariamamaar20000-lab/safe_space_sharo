import streamlit as st
import google.generativeai as genai
import random

# 1. إعداد مفتاح Gemini اللي إنت بعته
GOOGLE_API_KEY = "AIzaSyBN23Iip1T1gcTNhrNHerkWZYcDPwAzsLM"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Dr. Sharon | Safe Space", layout="centered")

# 2. التنسيق (Design)
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; direction: rtl; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #38bdf8; text-align: right; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #38bdf8; color: white; border: none; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌿 عيادة دكتور شارون الذكية</h1>", unsafe_allow_html=True)

# 3. الأزرار الذكية
col1, col2 = st.columns(2)
with col1:
    if st.button("💡 رسالة تحفيزية ذكية"):
        # هنا بنخلي Gemini نفسه هو اللي يألف الرسالة مش لستة قديمة
        prompt_quote = "اكتب رسالة تحفيزية قصيرة جداً وملهمة بالعامية المصرية لشخص بيمر بوقت صعب، خليها مختلفة وجديدة."
        try:
            response = model.generate_content(prompt_quote)
            st.info(response.text)
        except:
            st.info("إنت بطل وحكايتك لسه فيها فصول حلوة كتير..")

with col2:
    st.markdown('<a href="https://wa.me/201026330456" target="_blank"><button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; padding:10px; font-weight:bold; cursor:pointer;">📱 واتساب العيادة</button></a>', unsafe_allow_html=True)

# 4. نظام الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("احكي، أنا سامعك وبفهمك...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر..."):
        try:
            # تعليمات الشخصية (علاج نفسي + عامية مصرية)
            full_prompt = f"أنت دكتور شارون، معالج نفسي مصري شاطر وحنين. ردك يكون بالعامية المصرية الراقية، قدم نصيحة نفسية مختصرة ومريحة. المريض بيقول: {user_input}"
            response = model.generate_content(full_prompt)
            reply = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # إضافة خاصية "اسمع الرد" (صوت)
            audio_html = f'<audio autoplay src="https://translate.google.com/translate_tts?ie=UTF-8&q={reply[:200]}&tl=ar&client=tw-ob"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
            
            st.rerun()
        except Exception as e:
            st.error("المفتاح ده محتاج يتفعل من Google Cloud أو فيه ضغط، جرب كمان لحظة.")

if st.button("🗑️ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
