import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Safe Space | خبيرك النفسي", page_icon="🧠")
st.title("🧠 مستشارك النفسي الذكي")

# 2. حطيت لك المفتاح بتاعك هنا مباشرة عشان يشتغل حالاً
API_KEY = "AIzaSyDrvwbLS9l4_j0DkfsTmujF6E0e9Ki4E9Q"
genai.configure(api_key=API_KEY)

# 3. إعداد الموديل بأضمن اسم (flash-latest)
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "max_output_tokens": 8192,
}

# تعليمات الشخصية النفسية (صوت جيمناي)
system_instruction = (
    "أنت خبير في علم النفس، تتحدث بلهجة هادئة، داعمة، وذكية مثل Gemini. "
    "وظيفتك هي تقديم معلومات نفسية دقيقة بأسلوب بسيط ومريح للمستخدم. "
    "لا تعطي نصائح طبية نهائية بل قدم استشارات توعوية بلمسة إنسانية."
)

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest", 
  generation_config=generation_config,
  system_instruction=system_instruction
)

# 4. حفظ المحادثة
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطقة الدردشة
if prompt := st.chat_input("اتكلم معايا، أنا سامعك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # طلب الرد من جيمناي
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حصلت مشكلة بسيطة: {str(e)}")
