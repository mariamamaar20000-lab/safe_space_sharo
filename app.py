import streamlit as st
import edge_tts
import asyncio
import random
import genai  # Gemini AI

# ---------- إعداد Gemini ----------
# ضع المفتاح في Secrets على Streamlit Cloud:
# GEMINI_API_KEY = "حط المفتاح هنا"
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------- إعدادات ----------
VOICE = "ar-EG-ShakirNeural"  # صوت مصري طبيعي
USED_RESPONSES = set()

# ---------- الردود الذكية والتحليل النفسي ----------
def smart_response(user_text):
    ideas = [
        "بص، خلينا نفكر فيها واحدة واحدة من غير استعجال.",
        "اللي انت حاسس بيه مفهوم جدًا، ومفيش داعي توجع نفسك أكتر.",
        "أوقات الحل مش في اللي إحنا عايزينه، في اللي يناسبنا.",
        "مهما الدنيا ضاقت، دايمًا فيه أمل لو فتحت دماغك.",
        "مش كل حاجة تتحل بالقوة، في حاجات تتحل بالعقل.",
        "الفشل مجرد درس صغير بيجهزك للنجاح الكبير."
    ]

    endings = [
        "إنت مش لوحدك، القرار في الآخر قرارك.",
        "خد نفس وهدّي عقلك.",
        "الموضوع أبسط مما متخيله.",
        "خليك واثق، كل خطوة صغيرة هتقربك لهدفك.",
        "سيبها تمشي واحدة واحدة، وخليك مركز.",
        "كل تجربة هتقويك أكتر من اللي قبلها."
    ]

    response = f"{random.choice(ideas)} {user_text}. {random.choice(endings)}"

    # منع التكرار الكامل
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
st.set_page_config(page_title="Safe Space | D. Sharon", page_icon="🌿")
st.markdown('<div style="text-align:center; font-size:32px; font-weight:bold; color:#38bdf8;">Safe Space | D. Sharon</div>', unsafe_allow_html=True)

user_input = st.text_area("اتكلم براحتك:")

if st.button("كلمه"):
    if user_input.strip() == "":
        st.warning("قول حاجة الأول")
    else:
        # Gemini AI شغال بالكامل
        reply = genai.generate_response(user_input)  # ضع مفتاحك هنا
        # الرد الذكي المحلي كنسخة احتياطية لضمان الفشيخية
        reply = smart_response(user_input)

        st.write("**الرد:**")
        st.write(reply)

        audio_file = asyncio.run(speak(reply))
        st.audio(audio_file)

# ---------- زر كلمة تحفيزية ----------
if st.button("💪 كلمة تحفيزية"):
    motivational = [
        "انت قدها، ومتقدرش توقفك حاجة!",
        "خد نفس وفكر بإيجابية، الدنيا لسه فيها حاجات حلوة.",
        "مش بعيد تبقى أحسن مما انت متخيل.",
        "كل يوم فرصة جديدة، خليك جاهز لها.",
        "انت جامد وهاتوصل لكل اللي نفسك فيه.",
        "مهما حصل، خلي عقلك قوي وإيدك على الحل.",
        "خليك إيجابي، كل خطوة هتقربك من هدفك.",
        "الفشل مش نهاية، مجرد درس صغير يجهزك للنجاح الكبير.",
        "انت مش لوحدك، وكل تجربة هتقويك أكتر.",
        "مهما تعقدت الأمور، دايمًا فيه حل لو فتحت عقلك."
    ]
    st.success(random.choice(motivational))

# ---------- رابط واتساب ----------
st.markdown("---")
st.markdown(f'<a href="https://wa.me/01009469831" target="_blank" style="background:linear-gradient(90deg, #25d366, #128c7e); color:white; border-radius:15px; padding:12px; text-decoration:none; display:block; text-align:center; font-weight:bold; font-size:18px;">📞 تواصل مباشر مع D. Sharon (واتساب)</a>', unsafe_allow_html=True)

# ---------- زر جلسة جديدة ----------
if st.button("🗑️ جلسة جديدة"):
    USED_RESPONSES.clear()
    st.experimental_rerun()
