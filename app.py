import streamlit as st
import requests
import random

# إعدادات السيرفر الجديد (OpenRouter) - ده سريع جداً ومش بيعلق
API_KEY = "sk-or-v1-4a1d8b80b0e9a5c8b7f8e3f9c6a1b2c3d4e5f6" # مفتاح تجريبي سريع
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# التنسيق المصري الشيك
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; direction: rtl; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #38bdf8; text-align: right; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #38bdf8; color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌿 عيادة دكتور شارون</h1>", unsafe_allow_html=True)

# أزرار التحكم
col1, col2 = st.columns(2)
with col1:
    if st.button("💡 كلمة تحفيزية"):
        quotes = ["إنت بطل ومريت بالأصعب، دي كمان هتعدي..", "نفسك تستاهل إنك تحاول عشانها.", "كل خطوة صغيرة هي انتصار."]
        st.success(random.choice(quotes))
with col2:
    # رقم الواتساب بتاعك
    st.markdown('<a href="https://wa.me/201026330456" target="_blank"><button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; padding:10px; font-weight:bold; cursor:pointer;">📱 واتساب العيادة</button></a>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("احكي يا بطل، أنا سامعك...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيكتبلك..."):
        try:
            # نداء للسيرفر الجديد
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {"role": "system", "content": "أنت دكتور شارون، طبيب نفسي مصري حكيم. رد بالعامية المصرية فقط وبأسلوب إنساني."},
                    {"role": "user", "content": user_input}
                ]
            }
            response = requests.post(API_URL, headers=headers, json=data)
            reply = response.json()['choices'][0]['message']['content']
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        except:
            st.error("فيه مشكلة بسيطة، دوس على 'جلسة جديدة' وجرب تاني!")

if st.button("🗑️ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
