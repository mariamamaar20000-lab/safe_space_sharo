import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Safe Space")
st.title("🧠 مستشارك النفسي الذكي")

# قراءة المفتاح من الـ Secrets اللي صلحناها
try:
    API_KEY=st.secrets["AIzaSyDrvwbLS9l4_j0DkfsTmujF6E0e9Ki4E9Q"]
    genai.configure(api_key=API_KEY)
    # استخدام الموديل المستقر
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("تأكدي من كتابة API_KEY صح في صفحة Secrets")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("تحدث معي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

