import streamlit as st
from groq import Groq

# 1. الربط بمفتاح Groq الجديد (تم وضعه بنجاح)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# 2. تصميم واجهة دكتور شارون
st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-bottom: 15px; line-height: 1.6; }
    .title { color: #38bdf8; text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# 3. نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات القديم
for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# 4. منطقة الكلام والرد الفوري
user_input = st.chat_input("احكي يا بطل، أنا سامعك وبفهمك...")

if user_input:
    # حفظ رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيرد حالاً..."):
        try:
            # استخدام موديل Llama 3.3 (أسرع وأذكى موديل متاح حالياً)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "أنت دكتور شارون، طبيب نفسي مصري حكيم وشاطر جداً. رد بالعامية المصرية الراقية. تفاعل مع المريض، اسأله أسئلة ذكية تخليه يحكي أكتر، وواسيه بذكاء بشري. ممنوع تقول إنك ذكاء اصطناعي."},
                    *st.session_state.messages # عشان يفتكر الكلام اللي فات
                ],
            )
            reply = completion.choices[0].message.content
            
            # حفظ وعرض رد الدكتور
            st.session_state.messages.append({"role": "dr", "content": reply})
            st.markdown(f'<div class="chat-bubble"><b>د. شارون:</b> {reply}</div>', unsafe_allow_html=True)
            st.rerun()

        except Exception as e:
            st.error("فيه حاجة بسيطة وقفتنا، جرب تبعت كلامك تاني.")

# 5. زرار مسح الجلسة والواتساب
st.markdown("---")
if st.button("🗑️ ابدأ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
