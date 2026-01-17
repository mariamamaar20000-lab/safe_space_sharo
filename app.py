import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة المستخدم وتصميم الصفحة (ستايل هادئ)
st.set_page_config(page_title="Safe Space | خبيرك النفسي", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stApp { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 مستشارك النفسي الذكي")
st.caption("مساحة آمنة للحديث والحصول على معلومات نفسية داعمة بصوت وأسلوب Gemini")

# 2. وضع المفتاح مباشرة (API KEY)
API_KEY = "AIzaSyDrvwbLS9l4_j0DkfsTmujF6E0e9Ki4E9Q"
genai.configure(api_key=API_KEY)

# 3. تعليمات "الشخصية النفسية" (النبرة والأسلوب)
system_instruction = (
    "أنت خبير في علم النفس، تتحدث بلهجة هادئة، داعمة، وذكية جداً مثل Gemini. "
    "تستخدم كلمات مشجعة وتراعي مشاعر المستخدم بعمق. "
    "مهمتك تقديم معلومات نفسية دقيقة، وتوعية المستخدم بكيفية التعامل مع مشاعره، "
    "وتقديم استراتيجيات هدوء وتفاؤل. إذا كان السؤال طبياً بحت، وجهه بلطف لزيارة مختص."
)

# 4. إعداد الموديل بأحدث نسخة
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 5. إدارة الذاكرة (عشان يفتكر كلامك في نفس الجلسة)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. منطقة الإدخال والرد
if prompt := st.chat_input("أنا أسمعك.. بماذا تشعر؟"):
    # إضافة رسالة المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد من الخبير النفسي
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"حدث خطأ: تأكد أن ملف requirements.txt يحتوي على التحديثات. الخطأ: {str(e)}")
