import streamlit as st
import google.generativeai as genai

# 1. الربط المباشر بالمفتاح بتاعك (حطيتهولك جاهز يا دكتور)
API_KEY = "AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA"
genai.configure(api_key=API_KEY)

# 2. تصميم الواجهة (الاستايل الكحلي الفخم)
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-bottom: 15px; line-height: 1.6; }
    .title { color: #38bdf8; text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. تشغيل الذاكرة (عشان الدكتور يفتكر الكلام وياخد ويدي معاك)
if "chat_session" not in st.session_state:
    try:
        # بنستخدم موديل فلاش لأنه سريع جداً وبيرد فوراً
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state.chat_session = model.start_chat(history=[])
    except:
        # لو حصل ضغط، الموديل ده بديل مضمون
        model = genai.GenerativeModel('gemini-pro')
        st.session_state.chat_session = model.start_chat(history=[])

# 4. عرض الشات القديم
if "chat_session" in st.session_state:
    for message in st.session_state.chat_session.history:
        # بنخفي تعليمات السيستم عشان المريض ما يشوفهاش
        if "أنت دكتور شارون" in message.parts[0].text:
            continue
        role_label = "أنت" if message.role == "user" else "د. شارون"
        st.markdown(f'<div class="chat-bubble"><b>{role_label}:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)

# 5. منطقة الكلام والرد المصري الذكي
user_input = st.chat_input("فضفض، دكتور شارون سامعك...")

if user_input:
    # إظهار كلام المستخدم فوراً
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر في كلامك..."):
        try:
            # هنا بنفهم الذكاء الاصطناعي شخصيتك بالظبط
            prompt_instruction = (
                "أنت دكتور شارون، طبيب نفسي مصري شاطر وحكيم. "
                "رد بالعامية المصرية الراقية (بلاش لغة عربية فصحى). "
                "خُد وادي مع المريض في الكلام، اسأله عن تفاصيل مشكلته، وحسسه إنك إنسان حقيقي مش روبوت. "
                "لو حد قالك 'صباح الخير' أو 'إزيك' رد بترحيب مصري حار. "
                "المريض بيقول دلوقتي: " + user_input
            )
            
            response = st.session_state.chat_session.send_message(prompt_instruction)
            
            # عرض رد الدكتور
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {response.text}</div>', unsafe_allow_html=True)
            st.rerun() # تحديث عشان الشات يفضل منظم
            
        except Exception as e:
            st.error("فيه ضغط بسيط على السيستم، جرب تبعت رسالتك تاني يا بطل.")

# 6. زرار تصفية الشات والواتساب
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ ابدأ صفحة جديدة"):
        st.session_state.clear()
        st.rerun()
with col2:
    st.markdown(f'<a href="https://wa.me/201009469831" target="_blank" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">📞 واتساب د. شارون</div></a>', unsafe_allow_html=True)
