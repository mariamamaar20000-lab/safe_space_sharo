import streamlit as st
import google.generativeai as genai

# 1. الربط (AIzaSyAiX1ckt5kLlRVIl-dP9ad2YONj36itK-U)
genai.configure(api_key="YOUR_API_KEY_HERE")

# 2. التصميم (الكحلي اللي بنحبه)
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Safe Space | Dr. Sharon")

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. محرك الذكاء الاصطناعي (بدون فلسفة زيادة عشان يشتغل)
def ask_gemini(user_input):
    try:
        # استخدمنا الموديل الأضمن حالياً
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        full_prompt = f"أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية كأنك إنسان حقيقي وصديق. خُد وادي في الكلام وبلاش رسميات. المريض بيقولك: {user_input}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        # لو المفتاح فيه مشكلة، هيطبع لك السبب هنا عشان نعرفه
        return f"يا دكتور فيه مشكلة في الـ API: {str(e)}"

# 5. عرض الشات
for msg in st.session_state.messages:
    st.markdown(f'<div class="chat-bubble"><b>{"أنت" if msg["role"]=="user" else "د. شارون"}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# 6. الإدخال
user_input = st.chat_input("قول اللي في قلبك...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        with st.spinner("بيفكر..."):
            reply = ask_gemini(user_input)
            st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

