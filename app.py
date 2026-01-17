from google.generativeai import client as genai
import streamlit as st
import edge_tts
import asyncio
import random

# ---------- المفتاح هنا ----------
# استبدل كلمة YOUR_API_KEY_HERE بالمفتاح بتاعك
genai.configure(api_key="AIzaSyAiX1ckt5kLlRVIl-dP9ad2YONj36itK-U")

# ---------- إعدادات ----------
VOICE = "ar-EG-ShakirNeural"
USED_RESPONSES = set()

def smart_response(user_text):
    ideas = [
        "بص، خلينا نفكر فيها واحدة واحدة من غير استعجال.",
        "اللي انت حاسس بيه مفهوم جدًا، ومفيش داعي توجع نفسك أكتر.",
        "أوقات الحل مش في اللي إحنا عايزينه، في اللي يناسبنا."
    ]
    endings = [
        "إنت مش لوحدك، القرار في الآخر قرارك.",
        "خد نفس وهدّي عقلك.",
        "الموضوع أبسط مما متخيله."
    ]
    response = f"{random.choice(ideas)} {user_text}. {random.choice(endings)}"
    while response in USED_RESPONSES:
        response = f"{random.choice(ideas)} {user_text}. {random.choice(endings)}"
    USED_RESPONSES.add(response)
    return response

async def speak(text):
    file_name = "voice.mp3"
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(file_name)
    return file_name

# ---------- واجهة ----------
st.set_page_config(page_title="Safe is Best | D. Sharon", page_icon="🌿")
st.markdown('<div style="text-align:center; font-size:32px; font-weight:bold; color:#38bdf8;">Safe is Best | D. Sharon</div>', unsafe_allow_html=True)

user_input = st.text_area("اتكلم براحتك:")

if st.button("كلمه"):
    if user_input.strip() == "":
        st.warning("قول حاجة الأول")
    else:
        try:
            response = genai.generate_text(
                prompt=user_input,
                model="chat-bison-001"
            )
            reply = response["candidates"][0]["content"]
        except:
            reply = smart_response(user_input)

        st.write("**الرد:**")
        st.write(reply)

        audio_file = asyncio.run(speak(reply))
        st.audio(audio_file)

st.markdown("---")
st.markdown(f'<a href="https://wa.me/01009469831" target="_blank" style="background:linear-gradient(90deg, #25d366, #128c7e); color:white; border-radius:15px; padding:12px; text-decoration:none; display:block; text-align:center; font-weight:bold; font-size:18px;">📞 تواصل مباشر مع D. Sharon (واتساب)</a>', unsafe_allow_html=True)

if st.button("🗑️ جلسة جديدة"):
    USED_RESPONSES.clear()
    st.experimental_rerun()
