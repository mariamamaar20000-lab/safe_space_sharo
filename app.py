import streamlit as st
import google.generativeai as genai

# 1. الربط بالمفتاح الجديد (تم وضعه بنجاح)
API_KEY = "AIzaSyBN23Iip1T1gcTNhrNHerkWZYcDPwAzsLM"
genai.configure(api_key=API_KEY)

# 2. تصميم واجهة العيادة (اللون الكحلي الفخم)
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-bottom: 15px; line-height: 1.6; }
    .title { color: #38bdf8; text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    .stChatInput { background-color: #1e293b !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. تشغيل الذاكرة عشان الدكتور "ياخد ويدي" في الكلام
if "chat_session" not in st.session_state:
    try:
        # بنستخدم gemini-pro لأنه الأقوى في النقاشات النفسية
        model = genai.GenerativeModel('gemini-pro')
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"حصلت مشكلة بسيطة: {e}")

# 4. عرض المحادثة
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        # بنخفي التعليمات البرمجية عشان المريض ما يشوفهاش
        if "أنت دكتور شارون" in message.parts[0].text:
            continue
        role_label = "أنت" if message.role == "user" else "د. شارون"
        st.markdown(f'<div class="chat-bubble"><b>{role_label}:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)

# 5. منطقة الكلام والرد المصري الحكيم
user_input = st.chat_input("احكي يا بطل، دكتور شارون سامعك...")

if user_input:
    # عرض كلام المستخدم
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر في كلامك..."):
        try:
            # صياغة الشخصية المصرية
            prompt_instruction = (
                "أنت دكتور شارون، طبيب نفسي مصري حكيم. رد بالعامية المصرية الراقية. "
                "تفاعل مع المريض، ناقشه بذكاء، واسأله عن مشاعره بالتفصيل. "
                "خليك بشري ومريح جداً في الكلام. المريض بيقول: " + user_input
            )
            
            response = st.session_state.chat_session.send_message(prompt_instruction)
            
            # عرض رد الدكتور
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {response.text}</div>', unsafe_allow_html=True)
            st.rerun() # تحديث الصفحة عشان الكلام يترتب
            
        except Exception as e:
            st.error("السيرفر لسه بيقوم، جرب تبعت رسالتك كمان مرة يا بطل.")

# 6. أزرار التواصل ومسح الشات
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ ابدأ جلسة جديدة"):
        st.session_state.clear()
        st.rerun()
with col2:
    st.markdown(f'<a href="https://wa.me/201009469831" target="_blank" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">📞 واتساب د. شارون</div></a>', unsafe_allow_html=True)
