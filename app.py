import streamlit as st
import google.generativeai as genai

# نده المفتاح من الـ Secrets (أمان أكتر وذكاء)
try:
    api_key = st.secrets["AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA"]
    genai.configure(api_key=api_key)
except:
    st.error("يا دكتور، مفتاح الـ API مش موجود في الـ Secrets بتاعة Streamlit!")

# تصميم دكتور شارون
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-top: 10px; }
    .title { color: #38bdf8; text-align: center; font-weight: bold; font-size: 35px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# الذاكرة (عشان ياخد ويدي معاك)
if "chat" not in st.session_state:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state.chat = model.start_chat(history=[])
    except:
        st.error("المخ الذكي مش عارف يفتح، شيك على الـ API Key")

# عرض الرسايل
if "chat" in st.session_state:
    for message in st.session_state.chat.history:
        role = "أنت" if message.role == "user" else "د. شارون"
        st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {message.parts[0].text}</div>', unsafe_allow_html=True)

# خانة الكتابة
user_input = st.chat_input("احكي يا بطل، أنا سامعك وبفهمك...")

if user_input:
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيفكر في رد يريح بالك..."):
        try:
            # الشخصية المطلوبة
            instruction = f"أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية الراقية، ناقش المريض واسمع منه وخد وادي معاه بذكاء بشري. المريض بيقول: {user_input}"
            
            response = st.session_state.chat.send_message(instruction)
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {response.text}</div>', unsafe_allow_html=True)
            st.rerun()
        except:
            st.error("فيه حاجة وقفتنا، جرب تبعت كلامك تاني.")

# زرار تواصل مباشر
st.markdown("---")
st.markdown(f'<a href="https://wa.me/201009469831" target="_blank" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">📞 واتساب د. شارون المباشر</div></a>', unsafe_allow_html=True)
