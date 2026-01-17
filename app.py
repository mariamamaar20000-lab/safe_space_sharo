import streamlit as st
from groq import Groq

# 1. المفتاح بتاعك
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# التصميم الفخم
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🌿 Safe Space | Dr. Sharon</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>طبيب نفسي مصري - هنا عشان أسمعك وأشيل معاك</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    role_name = "أنت" if msg["role"] == "user" else "د. شارون"
    with st.chat_message(msg["role"]):
        st.write(f"**{role_name}:** {msg['content']}")

# منطقة الكلام
user_input = st.chat_input("احكي اللي في قلبك يا بطل...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(f"**أنت:** {user_input}")
    
    with st.spinner("دكتور شارون بيفكر في كلامك..."):
        try:
            # هنا بقى "سر الخلطة" في التعليمات:
            instruction = (
                "أنت دكتور شارون، طبيب نفسي مصري شاطر جداً وابن بلد. "
                "قاعدتك الذهبية: رد بالعامية المصرية الراقية المريحة، بلاش فصحى وبلاش لغة الروبوتات. "
                "ناقش المريض، اسأله أسئلة ذكية تخليه يحكي أكتر (زي: من امتى حاسس بكدة؟ طب وإيه كمان؟). "
                "خليك حنين في ردودك، واسيه، وحسسه إنك إنسان حقيقي وصديق قبل ما تكون دكتور. "
                "لو قالك 'تعبان' أو 'مخنوق' رد عليه برد يطمنه ويبدأ يحلل معاه السبب بالراحة. "
                "ممنوع تماماً تقول 'أنا نموذج لغة' أو 'أنا ذكاء اصطناعي'. إنت دكتور شارون وبس."
            )

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": instruction},
                    *st.session_state.messages
                ],
                temperature=0.8, # ده بيخلي الكلام "بشري" أكتر ومش نمطي
            )
            
            reply = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
            
        except Exception as e:
            st.error("العيادة زحمة شوية، ابعت رسالتك تاني حالا وهرد عليك!")

# زرار مسح الجلسة والبدء من جديد
if st.button("🗑️ ابدأ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
