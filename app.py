import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import time

# ---------- الربط ----------
# حط مفتاح الـ API بتاعك هنا
genai.configure(api_key="YOUR_API_KEY_HERE")

# إعداد الصوت
VOICE = "ar-EG-ShakirNeural"

# ---------- التصميم ----------
st.set_page_config(page_title="Safe Space | Dr. Sharon", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .main-title { font-size: 35px; color: #38bdf8; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-top: 10px; font-size: 18px; line-height: 1.6; }
    .whatsapp-btn { background: linear-gradient(90deg, #25d366, #128c7e) !important; color: white !important; border-radius: 15px; padding: 12px; text-decoration: none; display: block; text-align: center; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="main-title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# ---------- وظائف الصوت والذكاء ----------
async def generate_voice(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("response.mp3")
    return "response.mp3"

def get_ai_reply(user_input):
    try:
        # هنا بنشغل Gemini ونخليه ياخد ويدي براحته
        model = genai.GenerativeModel('gemini-pro')
        
        # دي أهم حتة: بنفهم جيميناي هو مين عشان يرد بالمصري وبذكاء
        context = f"""
        أنت الآن 'دكتور شارون'، طبيب نفسي مصري حكيم وشاطر جداً. 
        مهمتك: تسمع المريض بذكاء، ترد عليه بالعامية المصرية الراقية، تكون مقنع وبشري 100%. 
        لو المريض قال 'سلام عليكم' رد بترحيب مصري حار. 
        لو حكى مشكلة، حللها وناقشه فيها كأنك قاعد معاه في العيادة. 
        لو الموضوع خطير (زي الانتحار)، اتعامل بذكاء ودين وحكمة مصرية عشان تفرمله. 
        بلاش ردود آلية، خليك 'بني آدم' بياخد ويدي. 
        المريض بيقول: {user_input}
        """
        
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return "معلش يا صديقي، حصل ضغط على السيستم.. ممكن تعيد كلامك؟ أنا سامعك."

# ---------- عرض الشات ----------
for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# ---------- الإدخال ----------
with st.form("chat_form", clear_on_submit=True):
    u_input = st.text_input("اتفضل احكي، أنا سامعك...")
    submit = st.form_submit_button("إرسال")

if submit and u_input:
    st.session_state.messages.append({"role": "user", "content": u_input})
    
    with st.spinner("دكتور شارون بيفكر..."):
        reply = get_ai_reply(u_input)
        st.session_state.messages.append({"role": "dr", "content": reply})
        
        # تحويل الرد لصوت
        try:
            asyncio.run(generate_voice(reply))
        except:
            pass # لو الصوت علق ما يوقفش الشات
        
    st.rerun()

# تشغيل الصوت لآخر رسالة
if st.session_state.messages and st.session_state.messages[-1]["role"] == "dr":
    st.audio("response.mp3")

# ---------- الأزرار ----------
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ جلسة جديدة"):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.markdown(f'<a href="https://wa.me/201009469831" class="whatsapp-btn">📞 واتساب د. شارون</a>', unsafe_allow_html=True)
