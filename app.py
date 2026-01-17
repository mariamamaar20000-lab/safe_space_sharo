import streamlit as st
import google.generativeai as genai

# حط المفتاح الجديد هنا واتأكد إنه بين علامات التنصيص
genai.configure(api_key="AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA")

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.title("🧠 Safe Space | Dr. Sharon")

# تشغيل الذاكرة عشان "ياخد ويدي" معاك
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat_session = model.start_chat(history=[])

# عرض الشات القديم
for message in st.session_state.chat_session.history:
    role = "أنت" if message.role == "user" else "د. شارون"
    with st.chat_message(message.role):
        st.write(f"**{role}:** {message.parts[0].text}")

# خانة الكتابة
user_input = st.chat_input("احكي يا بطل، أنا سامعك...")

if user_input:
    with st.chat_message("user"):
        st.write(f"**أنت:** {user_input}")
    
    with st.spinner("دكتور شارون بيفكر..."):
        prompt = f"أنت دكتور شارون، دكتور نفسي مصري شاطر. رد بالعامية المصرية وبلاش رسميات، خليك زي الصديق وناقش المريض في كلامه. المريض بيقول: {user_input}"
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.write(f"**د. شارون:** {response.text}")
