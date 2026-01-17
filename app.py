import streamlit as st
import google.generativeai as genai

# 1. الربط المباشر
API_KEY="AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA"
genai.configure(api_key=API_KEY)

# 2. تصميم الواجهة
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-bottom: 15px; }
    .title { color: #38bdf8; text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. تشغيل الذاكرة بموديل سريع جداً (8b) عشان الضغط
if "chat_session" not in st.session_state:
    # الموديل ده أسرع بكتير ومش بيعلق
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    st.session_state.chat_session = model.start_chat(history=[])

# 4. عرض الشات
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        if "أنت دكتور شارون" in message.parts[0].text:
            continue
        role_label = "أنت" if message.role == "user" else "د. شارون"
        st.markdown(f'<div class="chat-bubble"><b>{role_label}:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)

# 5. منطقة الكلام
user_input = st.chat_input("فضفض، دكتور شارون سامعك...")

if user_input:
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيرد حالاً..."):
        try:
            # تعليمات الشخصية
            prompt_instruction = (
                "أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية الراقية. "
                "خُد وادي مع المريض بذكاء بشري، بلاش رسميات. المريض بيقول: " + user_input
            )
            
            # إرسال الرسالة
            response = st.session_state.chat_session.send_message(prompt_instruction)
            
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {response.text}</div>', unsafe_allow_html=True)
            st.rerun()
            
        except Exception as e:
            # لو الموديل السريع بردو علق (نادراً)، بنجرب الموديل المستقر
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                chat_alt = model_alt.start_chat(history=[])
                response = chat_alt.send_message(prompt_instruction)
                st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {response.text}</div>', unsafe_allow_html=True)
            except:
                st.error("السيستم عليه ضغط كبير دلوقتي، ارمي همومك وكلمني واتساب فوراً!")

# 6. الأزرار
st.markdown("---")
if st.button("🗑️ ابدأ صفحة جديدة"):
    st.session_state.clear()
    st.rerun()
