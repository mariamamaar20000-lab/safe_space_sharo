import streamlit as st
import requests

# 1. الربط بمفتاح Hugging Face اللي إنت لسه جايبه
HF_TOKEN = "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"

# موديل Mistral هو الأفضل حالياً في فهم السياق والرد بسرعة
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# تنسيق العيادة (عشان الكلام يبدأ من اليمين ويكون مريح)
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; direction: rtl; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #38bdf8; text-align: right; line-height: 1.6; }
    .title { color: #38bdf8; text-align: center; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 عيادة دكتور شارون</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for msg in st.session_state.messages:
    role_name = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role_name}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# منطقة الكلام والرد
user_input = st.chat_input("احكي يا بطل، أنا سامعك وبفهمك...")

if user_input:
    # حفظ رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر في رد يريح قلبك..."):
        try:
            # تعليمات الشخصية باللهجة المصرية
            prompt = f"<s>[INST] أنت دكتور شارون، طبيب نفسي مصري حكيم. رد بالعامية المصرية الراقية وبلاش لغة الروبوتات. اسمع المريض بقلبك ورد عليه رد يطمنه. المريض بيقول: {user_input} [/INST]"
            
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 500, "temperature": 0.7}})
            result = response.json()
            
            # تنظيف الرد من أي زوائد برمجية
            full_reply = result[0]['generated_text']
            reply = full_reply.split("[/INST]")[-1].strip()
            
            # حفظ وعرض رد الدكتور
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
            
        except Exception as e:
            st.error("السيرفر لسه بيقوم، ابعت رسالتك كمان مرة يا دكتور وهتشتغل!")

# زرار تصفية الشات
if st.button("🗑️ ابدأ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
