import streamlit as st
import requests
import random

# الإعدادات الأساسية
HF_TOKEN = "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"
# موديل Zephyr سريع جداً في الرد ومش بيسخن كتير
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# التنسيق (Design)
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; direction: rtl; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #38bdf8; text-align: right; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #38bdf8; color: white; font-weight: bold; }
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
    # حط رقمك هنا مكان الأصفار
    st.markdown('<a href="https://wa.me/201026330456" target="_blank"><button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; padding:10px; font-weight:bold; cursor:pointer;">📱 واتساب العيادة</button></a>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("احكي يا بطل...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.spinner("دكتور شارون بيكتبلك..."):
        try:
            prompt = f"<s>[INST] أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية الراقية: {user_input} [/INST]"
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            output = response.json()
            reply = output[0]['generated_text'].split("[/INST]")[-1].strip()
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        except:
            st.warning("السيرفر بيحمل الموديل، ابعت رسالتك كمان مرة دلوقتي وهتشتغل!")
