import streamlit as st
import google.generativeai as genai

# 1. الربط بمفتاح جيميناي (المفتاح ده أذكى بكتير في العربي)
API_KEY = "AIzaSyBN23Iip1T1gcTNhrNHerkWZYcDPwAzsLM"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Safe Space | Dr. Sharon", layout="centered")

# تصميم شيك وراقي
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 عيادة دكتور شارون")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for msg in st.session_state.messages:
    role_class = "د. شارون" if msg["role"] == "assistant" else "أنت"
    st.markdown(f'<div class="chat-bubble"><b>{role_class}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# منطقة الكلام
user_input = st.chat_input("قول يا بطل، سامعك...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble"><b>أنت:</b> {user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("دكتور شارون بيكتب رد عاقل..."):
        try:
            # هنا بقى سر الكلام المفهوم:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            full_prompt = (
                "أنت دكتور شارون، معالج نفسي مصري حكيم وراقي جداً. "
                "مهمتك: الرد بالعامية المصرية المفهومة البسيطة (زي كلامنا في الشارع المصري المتعلم). "
                "ممنوع تطلع حروف مشقلبة أو كلمات إنجليزي في وسط الكلام إلا للضرورة. "
                "ناقش المريض بحنان، اسأله عن تفاصيل مشاعره، وخليه يحس إنه بيكلم بني آدم مش آلة. "
                "المريض بيقول: " + user_input
            )
            
            response = model.generate_content(full_prompt)
            reply = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
            
        except Exception as e:
            st.error("فيه ضغط بسيط، ابعت رسالتك تاني حالا وهتشتغل!")

# زرار المسح
if st.button("🗑️ جلسة جديدة"):
    st.session_state.messages = []
    st.rerun()
