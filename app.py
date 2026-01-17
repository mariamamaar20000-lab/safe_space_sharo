import streamlit as st
import edge_tts
import asyncio
import random
import os
from datetime import datetime

# ---------- إعدادات ----------
VOICE = "ar-EG-ShakirNeural"  # صوت راجل مصري
USED_RESPONSES = set()

# ---------- الردود الذكية ----------
def smart_response(user_text):
    ideas = [
        "بص، خلينا نفكر فيها واحدة واحدة من غير استعجال.",
        "اللي انت حاسس بيه ده مفهوم، بس مش لازم ياخدك في سكة وحشة.",
        "أوقات الحل مش في اللي إحنا عايزينه، في اللي يناسبنا.",
        "خليني أقولك حاجة من غير تنظير.",
        "مش كل حاجة تتحل بالقوة، في حاجات تتحل بالعقل."
    ]

    endings = [
        "إنت مش لوحدك، بس القرار في الآخر قرارك.",
        "خد نفس كده، وفكر بهدوء.",
        "الموضوع أبسط مما متخيله.",
        "إنت فاهم أكتر ما إنت فاكر.",
        "سيبها تمشي واحدة واحدة."
    ]

    response = f"{random.choice(ideas)} {user_text}. {random.choice(endings)}"

    # منع التكرار
    while response in USED_RESPONSES:
        response = f"{random.choice(ideas)} {user_text}. {random.choice(endings)}"

    USED_RESPONSES.add(response)
    return response

# ---------- تحويل الكلام لصوت ----------
async def speak(text):
    file_name = "voice.mp3"
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(file_name)
    return file_name

# ---------- واجهة ----------
st.set_page_config(page_title="Safe is Best | Dr. Sharon", page_icon="🌿")
st.markdown('<div style="text-align:center; font-size:30px; font-weight:bold; color:#38bdf8;">Safe is Best | Dr. Sharon</div>', unsafe_allow_html=True)

user_input = st.text_area("اتكلم براحتك:")

if st.button("كلمه"):
    if user_input.strip() == "":
        st.warning("قول حاجة الأول")
    else:
        reply = smart_response(user_input)
        st.write("**الرد:**")
        st.write(reply)

        audio_file = asyncio.run(speak(reply))
        st.audio(audio_file)

# رابط واتساب
st.markdown("---")
st.markdown(f'<a href="https://wa.me/201009469831" target="_blank" style="background:linear-gradient(90deg, #25d366, #128c7e); color:white; border-radius:15px; padding:12px; text-decoration:none; display:block; text-align:center; font-weight:bold; font-size:18px;">📞 تواصل مباشر مع د. شارون (واتساب)</a>', unsafe_allow_html=True)

# زر جلسة جديدة
if st.button("🗑️ جلسة جديدة"):
    st.session_state.messages = []
    USED_RESPONSES.clear()
    st.experimental_rerun()
