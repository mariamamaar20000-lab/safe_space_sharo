import streamlit as st
import edge_tts
import asyncio
import random
import uuid
from datetime import datetime

# ================== الإعدادات ==================
VOICE = "ar-EG-ShakirNeural"  # صوت راجل مصري طبيعي
SESSION_ID = str(uuid.uuid4())

if "memory" not in st.session_state:
    st.session_state.memory = []

if "used_angles" not in st.session_state:
    st.session_state.used_angles = set()

# ================== التحليل النفسي ==================
def psychological_analysis(text):
    text = text.lower()

    states = {
        "ضغط": ["مضغوط", "زهقان", "مخنوق", "مش قادر", "تعبان"],
        "حيرة": ["مش عارف", "محتار", "تايه"],
        "غضب": ["متعصب", "مقروف", "غضبان"],
        "حزن": ["زعلان", "مكسور", "وحيد"],
        "خوف": ["خايف", "قلقان", "متوتر"]
    }

    detected = []
    for state, words in states.items():
        if any(w in text for w in words):
            detected.append(state)

    return detected if detected else ["عام"]

# ================== توليد زاوية جديدة ==================
def generate_angle(psych_state):
    angle_bank = {
        "ضغط": [
            "خلينا نفصل بين اللي في إيدك واللي برا سيطرتك",
            "الضغط لما يزيد، العقل بيحتاج تهوية مش قرارات",
            "مش كل حمل لازم يتشال دلوقتي"
        ],
        "حيرة": [
            "الحيرة معناها إنك فاهم أكتر من اختيار",
            "مش لازم تختار دلوقتي",
            "أوقات عدم القرار هو قرار ذكي"
        ],
        "غضب": [
            "الغضب طاقة، يا إما تكسر يا إما تبني",
            "مش كل حاجة تستاهل رد فعل",
            "سكوتك أحيانًا أقوى من أي رد"
        ],
        "حزن": [
            "الحزن مش ضعف، ده دليل إحساس",
            "الوجع مش عدوك، بس مينفعش يسوقك",
            "فيه حاجات بتوجع عشان تنضج"
        ],
        "خوف": [
            "الخوف بيحمي أكتر ما بيأذي",
            "مش كل خوف إنذار حقيقي",
            "أنت أقوى من السيناريوهات اللي في دماغك"
        ],
        "عام": [
            "خلينا نبص للصورة الكبيرة",
            "مش كل سؤال محتاج إجابة دلوقتي",
            "الفهم أهم من الحل السريع"
        ]
    }

    for _ in range(10):
        angle = random.choice(angle_bank[psych_state])
        if angle not in st.session_state.used_angles:
            st.session_state.used_angles.add(angle)
            return angle

    return random.choice(angle_bank[psych_state])

# ================== الرد الذكي ==================
def smart_response(user_text):
    states = psychological_analysis(user_text)
    main_state = states[0]

    angle = generate_angle(main_state)

    openers = [
        "خليني أتكلم معاك بهدوء",
        "اسمعني للآخر",
        "تعالى نبص للموضوع من زاوية مختلفة",
        "خلينا نهدى الأول"
    ]

    closers = [
        "خد وقتك، مش مستعجلين",
        "أنا هنا مكمل معاك",
        "الكلام ده مش نصيحة، ده تفكير مشترك",
        "اللي حاسس بيه له حق"
    ]

    response = (
        f"{random.choice(openers)}. "
        f"{angle}. "
        f"من كلامك واضح إنك بتمر بحالة {main_state}. "
        f"وده طبيعي جدًا في المرحلة دي. "
        f"{random.choice(closers)}."
    )

    st.session_state.memory.append({
        "time": datetime.now().isoformat(),
        "input": user_text,
        "state": main_state,
        "response": response
    })

    return response

# ================== الصوت ==================
async def speak(text):
    file_name = f"voice_{SESSION_ID}.mp3"
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(file_name)
    return file_name

# ================== الواجهة ==================
st.set_page_config(page_title="AI نفسي مصري", page_icon="🧠", layout="centered")
st.title("🧠 دكتور نفسي ذكي – مصري")

user_input = st.text_area("اتكلم براحتك، من غير تفكير:")

if st.button("اتكلم"):
    if user_input.strip() == "":
        st.warning("اكتب حاجة الأول")
    else:
        reply = smart_response(user_input)
        st.markdown("### الرد:")
        st.write(reply)

        audio_file = asyncio.run(speak(reply))
        st.audio(audio_file)

if st.button("جلسة جديدة"):
    st.session_state.memory = []
    st.session_state.used_angles = set()
    st.experimental_rerun()
