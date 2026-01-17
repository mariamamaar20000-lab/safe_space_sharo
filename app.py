import streamlit as st
import google.generativeai as genai

# 1. الربط بالمفتاح الجديد (الصاروخ)
API_KEY = "AIzaSyBN23Iip1T1gcTNhrNHerkWZYcDPwAzsLM"
genai.configure(api_key=API_KEY)

# 2. تصميم واجهة دكتور شارون
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-bottom: 15px; }
    .title { color: #38bdf8; text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. نظام الذاكرة البسيط (عشان ما يهنجش)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات القديم
for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# 4. منطقة الكلام والرد
user_input = st.chat_input("فضفض يا بطل، أنا سامعك...")

if user_input:
    # حفظ رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيرد عليك..."):
        try:
            # استخدام أسرع موديل (Flash)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # الأمر اللي بيخليه بشري ومصري
            instruction = (
                "أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية الراقية. "
                "ناقش المريض في كلامه وخد وادي معاه كأنك صديق وفي عيادة حقيقية. "
                "المريض بيقول: " + user_input
            )
            
            response = model.generate_content(instruction)
            reply = response.text
            
            # حفظ وعرض رد الدكتور
            st.session_state.messages.append({"role": "dr", "content": reply})
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {reply}</div>', unsafe_allow_html=True)
            st.rerun()

        except Exception as e:
            # لو الموديل لسه بيقوم، بنطلع رد ذكي بدل الشاشة الحمرا
            st.info("دكتور شارون بياخد نفسه.. ابعت الرسالة تاني حالا وهتشتغل!")

# 5. زرار مسح الجلسة
if st.button("🗑️ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
