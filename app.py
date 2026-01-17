import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import time

# ---------- الإعدادات والربط ----------
# حط مفتاح الـ API بتاعك هنا
genai.configure(api_key="YOUR_API_KEY_HERE")

# إعداد الصوت
VOICE = "ar-EG-ShakirNeural"

# ---------- واجهة المستخدم (التصميم الكحلي) ----------
st.set_page_config(page_title="Safe Space | Dr. Sharon", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    .main-title { font-size: 35px; color: #38bdf8; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .chat-bubble { background-color: #1e293b; padding: 15px; border-radius: 15px; border-right: 5px solid #38bdf8; margin-top: 10px; font-size: 18px; line-height: 1.6; }
    .whatsapp-btn { background: linear-gradient(90deg, #25d366, #128c7e) !important; color: white !important; border-radius: 15px; padding: 12px; text-decoration: none; display: block; text-align: center; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# ذاكرة الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="main-title">🌿 Safe Space | Dr. Sharon</div>', unsafe_allow_html=True)

# ---------- وظائف الصوت والذكاء ----------
async def generate_voice(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("response.mp3")
    return "response.mp3"

def get_ai_reply(user_input):
    # نظام الحماية اللي طلبته (الانتحار والأهل) قبل ما نبعت للذكاء الاصطناعي
    text = user_input.lower()
    if any(w in text for w in ["انتحر", "اموت", "انهي حياتي"]):
        return "يا صديقي، استغفر الله.. حياتك غالية أوي وعند ربنا كبيرة. الوجع بكرة يخلص بس روحك لو راحت مش هترجع. أنا جنبك، كلمني واتساب حالاً وخلينا نعدي اللحظة دي سوا. ❤️"
    
    if "أهل" in text or "اهل" in text or "سيب البيت" in text:
        return "سيبان البيت مش هو الحل اللي هيريحك، المواجهة أو حتى الهدوء دلوقتي أهم. احكي لي إيه اللي حصل في البيت بالظبط وموصلك لكدة؟ أنا سامعك للأخر. 🏠"

    try:
        # محرك جيميناي
        model = genai.GenerativeModel('gemini-pro')
        # بنعطيه تعليمات يمثل دورك
        prompt = f"أنت الدكتور شارون، طبيب نفسي مصري حكيم. رد على المريض بالعامية المصرية بأسلوب محتوي وذكي ومقنع. المريض بيقول: {user_input}"
        response = model.generate_content(prompt)
        return response.text
    except:
        return "كلامك محتاج تفكير عميق.. أنا معاك وسامعك، كمل حكايتك يا بطل. 😊"

# ---------- عرض الشات ----------
for msg in st.session_state.messages:
    role = "أنت" if msg["role"] == "user" else "د. شارون"
    st.markdown(f'<div class="chat-bubble"><b>{role}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# ---------- منطقة الإدخال ----------
with st.form("chat_form", clear_on_submit=True):
    u_input = st.text_input("فضفض لدكتور شارون...")
    submit = st.form_submit_button("إرسال")

if submit and u_input:
    # حفظ رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": u_input})
    
    with st.spinner("دكتور شارون بيفكر وبيجهز الرد..."):
        # جلب الرد
        reply = get_ai_reply(u_input)
        st.session_state.messages.append({"role": "dr", "content": reply})
        
        # تحويل الرد لصوت
        audio_file = asyncio.run(generate_voice(reply))
        
    st.rerun()

# تشغيل الصوت لآخر رسالة فقط
if st.session_state.messages and st.session_state.messages[-1]["role"] == "dr":
    st.audio("response.mp3")

# ---------- الأزرار السفلية ----------
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ جلسة جديدة"):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.markdown(f'<a href="https://wa.me/201009469831" class="whatsapp-btn">📞 واتساب د. شارون</a>', unsafe_allow_html=True)
