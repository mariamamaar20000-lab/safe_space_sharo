import streamlit as st
import google.generativeai as genai

# 1. حط مفتاح الـ API بتاعك هنا (تأكد إنه بين علامات التنصيص ومفيش مسافات)
MY_API_KEY = "AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA"

try:
    genai.configure(api_key=MY_API_KEY)
except Exception as e:
    st.error(f"خطأ في إعداد المفتاح: {e}")

# 2. تصميم الواجهة
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-top: 10px; }
    .main-title { font-size: 35px; color: #38bdf8; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. تهيئة الجلسة
if "chat_session" not in st.session_state:
    try:
        # استخدمنا gemini-1.5-flash لأنه الأسرع والأضمن حالياً
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"مشكلة في تشغيل الموديل: {e}")

# 4. عرض الشات
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        role = "أنت" if message.role == "user" else "د. شارون"
        st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)

# 5. الإدخال والرد
user_input = st.chat_input("احكي يا بطل، أنا سامعك...")

if user_input:
    # إظهار رسالة المستخدم
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر..."):
        try:
            # الأمر اللي بيخلي الذكاء الاصطناعي "ياخد ويدي" بالمصري
            instruction = f"أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية وبلاش رسميات، خليك زي الصديق وناقش المريض في كلامه وافتح معاه مواضيع. المريض بيقول: {user_input}"
            
            response = st.session_state.chat_session.send_message(instruction)
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {response.text}</div>', unsafe_allow_html=True)
            st.rerun()
            
        except Exception as e:
            # هنا هيطبع لك الخطأ بالظبط عشان نعرف نحله لو استمرت المشكلة
            st.error(f"حصل خطأ أثناء الرد: {e}")

if st.button("🗑️ جلسة جديدة"):
    st.session_state.clear()
    st.rerun()
