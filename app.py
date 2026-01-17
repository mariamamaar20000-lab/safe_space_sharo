import streamlit as st
import google.generativeai as genai

# إعداد واجهة البرنامج
st.set_page_config(page_title="Safe Space", page_icon="🧠")
st.title("🧠 مستشارك النفسي الذكي")

# 1. إعداد المفتاح من Secrets
API_KEY = st.secrets["AIzaSyDrvwbLS9l4_j0DkfsTmujF6E0e9Ki4E9Q"]
genai.configure(api_key=API_KEY)

# 2. إعداد الموديل
# تأكدي أن الأسطر التالية تبدأ من أول السطر بدون مسافات إضافية
system_instruction = "أنت خبير في علم النفس، تتحدث بلهجة هادئة وداعمة."

model = genai.GenerativeModel(
    model_name="gemini-pro"
)

# 3. حفظ المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. صندوق الدردشة
if prompt := st.chat_input("تحدث معي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
