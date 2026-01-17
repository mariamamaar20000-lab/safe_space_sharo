import streamlit as st
import requests

# المفتاح اللي إنت جبته وشغال 100%
HF_TOKEN = "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"
# موديل خفيف وسريع جداً عشان ما يطلعش رسالة "السيرفر بيقوم"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Safe Space | Dr. Sharon")

st.markdown("<h1 style='text-align: center;'>🌿 عيادة دكتور شارون</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# منطقة الكلام
user_input = st.chat_input("احكي يا بطل...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.spinner("دكتور شارون بيرد..."):
        try:
            # تعليمات بسيطة للموديل
            payload = {"inputs": f"<s>[INST] أنت دكتور نفسي مصري اسمه شارون. رد بالعامية المصرية: {user_input} [/INST]"}
            response = requests.post(API_URL, headers=headers, json=payload)
            output = response.json()
            
            # استخراج الرد
            reply = output[0]['generated_text'].split("[/INST]")[-1].strip()
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        except:
            st.error("السيرفر لسه بيسخن، ابعت رسالتك تاني حالا وهتشتغل!")
