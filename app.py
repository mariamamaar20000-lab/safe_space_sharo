import streamlit as st
import google.generativeai as genai

# 1. إعداد الربط (تأكد من وضع مفتاحك هنا)
genai.configure(api_key="AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA")

# 2. تصميم الواجهة الكحلي
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-top: 10px; line-height: 1.6; }
    .main-title { font-size: 35px; color: #38bdf8; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .whatsapp-btn { background: linear-gradient(90deg, #25d366, #128c7e) !important; color: white !important; border-radius: 15px; padding: 12px; text-decoration: none; display: block; text-align: center; font-weight: bold; font-size: 18px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. تشغيل الذاكرة (Chat Session) بموديل مضمون
if "chat_session" not in st.session_state:
    try:
        # استخدمنا models/gemini-1.5-flash كاسم رسمي وأضمن
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"حصلت مشكلة في تشغيل المخ الذكي: {e}")

# 4. عرض الرسائل القديمة
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        # تجاهل تعليمات النظام المخفية
        if "أنت دكتور شارون" in message.parts[0].text:
            continue
        role_label = "أنت" if message.role == "user" else "د. شارون"
        st.markdown(f'<div class="chat-bubble"><b>{role_label}:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)

# 5. منطقة الإدخال والرد
user_input = st.chat_input("احكي يا بطل، دكتور شارون سامعك...")

if user_input:
    # عرض رسالة المستخدم فوراً
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر..."):
        try:
            # صياغة الطلب ليكون "بياخد وبيدي"
            prompt = f"أنت دكتور شارون، طبيب نفسي مصري حكيم وبشري. رد بالعامية المصرية الراقية، ناقشني وخد وادي معايا في الكلام كأننا في عيادة. ردي على: {user_input}"
            
            response = st.session_state.chat_session.send_message(prompt)
            
            # عرض رد الدكتور
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {response.text}</div>', unsafe_allow_html=True)
            st.rerun() # تحديث عشان الشات يترتب
            
        except Exception as e:
            st.error("فيه حاجة بسيطة وقفتنا، جرب تبعت الرسالة تاني كدة؟")

# 6. زرار الواتساب للتواصل المباشر
st.markdown("---")
st.markdown(f'<a href="https://wa.me/201009469831" target="_blank" class="whatsapp-btn">📞 تواصل مباشر مع د. شارون (واتساب)</a>', unsafe_allow_html=True)

if st.button("🗑️ جلسة جديدة"):
    st.session_state.clear()
    st.rerun()
