import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import os

# ---------- الربط الفعلي ----------
# تأكد إنك حاطط المفتاح الصح هنا
genai.configure(api_key="YOUR_API_KEY_HERE")

# إعداد الصوت المصري
VOICE = "ar-EG-ShakirNeural"

# ---------- واجهة المستخدم ----------
st.set_page_config(page_title="Safe Space | Dr. Sharon", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .main-title { font-size: 38px; color: #38bdf8; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .chat-bubble { background-color: #1e293b; padding: 18px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-top: 10px; font-size: 18px; line-height: 1.7; box-shadow: 2px 2px 10px rgba(0,0,0,0.2); }
    .whatsapp-btn { background: linear-gradient(90deg, #25d366, #128c7e) !important; color: white !important; border-radius: 15px; padding: 12px; text-decoration: none; display: block; text-align: center; font-weight: bold; font-size: 18px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ذاكرة الشات المستمرة
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="main-title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# ---------- وظائف الصوت والذكاء ----------
async def generate_voice(text):
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save("response.mp3")
        return True
    except:
        return False

def get_ai_reply(user_input):
    try:
        # استخدام أحدث موديل من جيميناي
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # تعليمات الشخصية (System Instructions)
        prompt = f"""
        أنت الآن 'دكتور شارون'، طبيب نفسي مصري حكيم جداً وبشري.
        ممنوع ترد ردود آلية. خد وادي مع المريض في الكلام.
        اتكلم عامية مصرية بتاعة ولاد بلد، زي 'يا غالي'، 'منورني'، 'احكي لي يا بطل'.
        لو حد سلم عليك رد بذكاء، لو حد حكى مشكلة ناقشه في تفاصيلها كأنك قاعد معاه.
        لو المشكلة دينية أو انتحارية، استخدم حكمتك ودينك المصري عشان تقنعه وتطمنه.
        ممنوع تقول 'أنا ذكاء اصطناعي'.. أنت دكتور شارون وبس.
        دي الرسالة اللي جاتلك من المريض دلوقتي: {user_input}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # رد ذكي حتى لو حصل خطأ تقني
        return "بقولك إيه.. الكلام ده محتاج تركيز عالي مني، ارمي اللي وراك وقولي تاني بالراحة كدة إيه اللي شاغل بالك؟"

# ---------- عرض الشات ----------
for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# ---------- منطقة الإدخال ----------
with st.form("chat_form", clear_on_submit=True):
    u_input = st.text_input("فضفض، أنا سامعك بكل جوارحي...")
    submit = st.form_submit_button("ارسل لدكتور شارون")

if submit and u_input:
    st.session_state.messages.append({"role": "user", "content": u_input})
    
    with st.spinner("دكتور شارون بيفكر في كلامك..."):
        reply = get_ai_reply(u_input)
        st.session_state.messages.append({"role": "dr", "content": reply})
        
        # تحويل الرد لصوت (اختياري)
        asyncio.run(generate_voice(reply))
        
    st.rerun()

# تشغيل الصوت لآخر رسالة
if st.session_state.messages and st.session_state.messages[-1]["role"] == "dr":
    if os.path.exists("response.mp3"):
        st.audio("response.mp3")

# ---------- الأزرار ----------
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ ابدأ صفحة جديدة"):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.markdown(f'<a href="https://wa.me/201009469831" class="whatsapp-btn">📞 واتساب د. شارون</a>', unsafe_allow_html=True)
