import streamlit as st
from groq import Groq

# 1. المفتاح بتاعك (تأكد إنك دوست Allow Secret في GitHub)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# التصميم
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌿 Safe Space | Dr. Sharon</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# منطقة الكلام
user_input = st.chat_input("احكي يا بطل، أنا سامعك...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.spinner("دكتور شارون بيفكر في كلامك..."):
        try:
            # استخدمت لك موديل Llama-3.1-8b لأنه طلقة ومستقر جداً
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[
                    {"role": "system", "content": "أنت دكتور شارون، طبيب نفسي مصري. رد بالعامية المصرية الراقية. تفاعل مع المريض وواسيه بذكاء."},
                    *st.session_state.messages
                ],
            )
            reply = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
        except Exception as e:
            st.error("العيادة زحمة شوية، ابعت رسالتك تاني حالا وهرد عليك!")
