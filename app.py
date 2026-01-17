import streamlit as st
import requests
import random

# 1. الإعدادات والمفاتيح
HF_TOKEN = "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"
# الموديل ده "طلقة" ومش بيحتاج تسخين كتير
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# 2. التنسيق (Design)
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; direction: rtl; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #38bdf8; text-align: right; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #38bdf8; color: white; font-weight: bold; }
    .whatsapp-btn { background-color: #25d366 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌿 عيادة دكتور شارون</h1>", unsafe_allow_html=True)

# 3. أزرار التحكم السريعة
col1, col2 = st.columns(2)

with col1:
    if st.button("💡 كلمة تحفيزية"):
        quotes = [
            "إنت بطل ومريت بالأصعب، دي كمان هتعدي..",
            "نفسك تستاهل إنك تحاول عشانها مرة وعشرة.",
            "مش لازم تكون مثالي، كفاية إنك حقيقي.",
            "كل خطوة صغيرة بتعملها النهاردة هي انتصار كبير لبكرة."
        ]
        st.info(random.choice(quotes))

with col2:
    # حط رقم واتساب العيادة هنا مكان الزيرو
    whatsapp_link = "https://wa.me/201234567890" 
    st.markdown(f'<a href="{whatsapp_link}" target="_blank"><button style="width:100%; border-radius:20px; background-color:#25d366; color:white; border:none; padding:10px; font-weight:bold; cursor:pointer;">📱 واتساب العيادة</button></a>', unsafe_allow_html=True)

st.divider()

# 4. نظام الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("احكي يا بطل، أنا سامعك...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيكتبلك..."):
        try:
            # نظام التعليمات (Prompt)
            prompt = f"<s>[INST] أنت دكتور شارون، طبيب نفسي مصري حكيم. رد بالعامية المصرية الراقية كأنك في عيادة. المريض بيقول: {user_input} [/INST]"
            
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            output = response.json()
            
            # استخراج الرد وتنظيفه
            full_text = output[0]['generated_text']
            reply = full_text.split("[/INST]")[-1].strip()
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        except:
            st.warning("السيرفر بيحمل الموديل بس، ابعت رسالتك كمان مرة دلوقتي وهتشتغل فوراً!")

# زرار مسح الجلسة
if st.button("🗑️ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
