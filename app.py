import streamlit as st
import google.generativeai as genai

# 1. إعداد الصفحة في Streamlit
st.set_page_config(page_title="Safe Space | خبيرك النفسي", page_icon="🧠")
st.title("🧠 مستشارك النفسي الذكي")
st.caption("أنا هنا لأسمعك وأقدم لك معلومات نفسية تدعمك")

# 2. ربط مفتاح الـ API من الـ Secrets
try:
    genai.configure(api_key=st.secrets["API_KEY"])
except Exception as e:
    st.error("خطأ: لم يتم العثور على مفتاح الـ API. تأكد من إضافته في Secrets.")

# 3. إعداد الموديل (تم تحديث الاسم لضمان عدم حدوث NotFound)
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

# هنا بنحدد شخصية البوت (طريقتي في الكلام)
system_instruction = (
    "أنت خبير في علم النفس، تتحدث بلهجة هادئة، داعمة، وذكية مثل Gemini. "
    "وظيفتك هي تقديم معلومات نفسية دقيقة بأسلوب بسيط ومريح للمستخدم. "
    "تجنب التشخيص الطبي القاطع، وشجع المستخدم دائماً على التفاؤل والبحث عن المعرفة."
)

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash", # الموديل الأحدث والمستقر
  generation_config=generation_config,
  system_instruction=system_instruction
)

# 4. إدارة سجل المحادثة (عشان يفتكر كلامك)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. واجهة المستخدم للدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف تشعر اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # إرسال الرسالة للموديل
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {str(e)}")
