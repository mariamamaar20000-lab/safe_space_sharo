import streamlit as st
import google.generativeai as genai

# إعداد واجهة البرنامج
st.set_page_config(page_title="Safe Space", page_icon="🧠")
st.title("🧠 مستشارك النفسي الذكي")

# 1. وضع مفتاح الـ API مباشرة
API_KEY = "AIzaSyDrvwbLS9l4_j0DkfsTmujF6E0e9Ki4E9Q"
genai.configure(api_key=API_KEY)

# 2. إعداد الموديل بتعليمات الشخصية النفسية
system_instruction = (
    "أنت خبير في علم النفس، تتحدث بلهجة هادئة وداعمة وذكية مثل Gemini. "
    "وظيفتك تقديم معلومات نفسية دقيقة ودعم المستخدم بكلمات تفاؤلية."
)

# استخدمنا flash-latest لضمان أعلى توافق وحل مشكلة الـ 404
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=system_instruction
)

# 3. حفظ المحادثة في الذاكرة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. صندوق الدردشة والرد
if prompt := st.chat_input("تحدث معي، أنا أسمعك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # طلب الرد من الموديل
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"خطأ تقني: {str(e)}")
            st.info("تأكد من رفع ملف requirements.txt لضمان عمل البرنامج.")
