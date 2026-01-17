import streamlit as st
import google.generativeai as genai

# ================== إعداد الصفحة ==================
st.set_page_config(
    page_title="Safe Space",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 مستشارك النفسي الذكي")
st.caption("مساحة آمنة للفضفضة والدعم 🤍")

# ================== التأكد من API KEY ==================
if "API_KEY" not in st.secrets:
    st.error("❌ API_KEY مش موجود في Streamlit Secrets")
    st.stop()

# ================== إعداد Gemini ==================
try:
    genai.configure(api_key=st.secrets["API_KEY"])
    # ✅ السطر الصح للموديل بعد تثبيت آخر نسخة
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"خطأ في إعداد Gemini: {e}")
    st.stop()

# ================== System Prompt ==================
SYSTEM_PROMPT = """
أنت مستشار نفسي داعم.
بتتكلم باللهجة المصرية بهدوء واحترام.
بتسمع أكتر ما بتتكلم، ومش بتحكم على اللي قدامك.
"""

# ================== Session State ==================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": SYSTEM_PROMPT}
    ]

# ================== عرض المحادثة ==================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================== إدخال المستخدم ==================
if prompt := st.chat_input("أنا هنا بسمعك.. تحب تحكي عن إيه؟"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]}
                for m in st.session_state.messages
            ])

            response = chat.send_message(prompt)
            reply = response.text or "أنا معاك، خد وقتك واحكي 🤍"

            st.markdown(reply)
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        except Exception as e:
            st.error(f"حصل خطأ أثناء الرد: {e}")

# ================== زر مسح المحادثة ==================
if st.button("🗑️ مسح المحادثة"):
    st.session_state.messages = [
        {"role": "user", "content": SYSTEM_PROMPT}
    ]
    st.experimental_rerun()
