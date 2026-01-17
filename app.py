import streamlit as st
import google.generativeai as genai
import random

# 1. الربط (المفتاح بتاعك أهو)
API_KEY = "AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA"
genai.configure(api_key=API_KEY)

# 2. تصميم الواجهة
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-bottom: 15px; }
    .title { color: #38bdf8; text-align: center; font-size: 32px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. ردود الطوارئ (لو السيستم وقع الدكتور مش هيسكت)
emergency_replies = [
    "بص يا بطل، الكلام ده كبير ومحتاج مننا قعدة رايقة، قولي أكتر إيه اللي شاغل بالك دلوقتي؟",
    "أنا سامعك وحاسس بيك جداً، كمل أنا معاك للأخر.. إيه كمان مضايقك؟",
    "فضفض وطلع كل اللي جواك، أنا هنا عشانك ومش هسيبك، احكي لي بالتفصيل.",
    "كلامك لمس قلبي.. قولي، تفتكر إيه أول خطوة ممكن تخليك أحسن دلوقتي؟"
]

# 4. الذاكرة
if "chat" not in st.session_state:
    st.session_state.chat = []

# 5. عرض الشات
for msg in st.session_state.chat:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# 6. الإدخال والرد "المضاد للتعليق"
user_input = st.chat_input("احكي، أنا سامعك...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر..."):
        try:
            # محاولة الكلام مع جيميناي
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"أنت دكتور نفسي مصري حكيم اسمه شارون. رد بالعامية المصرية وناقش المريض في كلامه: {user_input}"
            response = model.generate_content(prompt)
            reply = response.text
        except:
            # لو السيستم وقع، بنطلع رد من ردود الطوارئ الذكية
            reply = random.choice(emergency_replies)

        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {reply}</div>', unsafe_allow_html=True)
        st.rerun()

st.markdown("---")
if st.button("🗑️ جلسة جديدة"):
    st.session_state.chat = []
    st.rerun()
