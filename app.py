import streamlit as st
import google.generativeai as genai

# سحب المفتاح من Secrets بأمان
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["AIzaSyC5iDd3NlSQSMPmKJfPsV7QD0joxEeT_LA"])
else:
    st.error("يا دكتور، أنت لسه ما حطيتش المفتاح في الـ Secrets!")

st.title("🌿 Safe Space | Dr. Sharon")

# تشغيل الذاكرة
if "chat" not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat = model.start_chat(history=[])

# عرض المحادثة
for message in st.session_state.chat.history:
    role = "أنت" if message.role == "user" else "د. شارون"
    st.chat_message(message.role).write(f"**{role}:** {message.parts[0].text}")

# خانة الكتابة
user_input = st.chat_input("احكي يا بطل...")

if user_input:
    st.chat_message("user").write(f"**أنت:** {user_input}")
    
    # الرد الذكي
    prompt = f"أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية وبلاش رسميات، ناقش المريض وخد وادي معاه. ردي على: {user_input}"
    response = st.session_state.chat.send_message(prompt)
    
    st.chat_message("assistant").write(f"**د. شارون:** {response.text}")
    st.rerun()
