import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Safe Space", page_icon="🧠")
st.title("🧠 مستشارك النفسي الذكي")

# تأكدي إن الكلمة هنا هي "API_KEY" فقط
if "API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["API_KEY"])
        
        # استخدمي الاسم ده بالتحديد، ده اللي هيحل مشكلة الـ 404
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("أنا هنا بسمعك.. حابة تحكي عن إيه؟"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # طلب الرد
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"حصل خطأ بسيط: {e}")
else:
    st.warning("رجاءً تأكدي من تسمية المفتاح API_KEY في صفحة Secrets.")
