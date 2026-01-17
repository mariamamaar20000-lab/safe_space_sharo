import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Safe Space", page_icon="🧠")
st.title("🧠 مستشارك النفسي الذكي")

# التأكد من وجود المفتاح
if "API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["AIzaSyDrvwbLS9l4_j0DkfsTmujF6E0e9Ki4E9Q"])
        
        # 1. إعداد الموديل مع "تعليمات النظام" عشان يتقمص الشخصية
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="أنت مستشار نفسي خبير، تمتاز بالهدوء والتعاطف. وظيفتك الاستماع للمستخدم وتقديم دعم نفسي وإرشادات عملية. ردودك يجب أن تكون دافئة وباللهجة التي يفضلها المستخدم."
        )

        # إعداد ذاكرة المحادثة في Streamlit
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # عرض الرسائل السابقة من الـ session_state
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # صندوق إدخال المستخدم
        if prompt := st.chat_input("أنا هنا بسمعك.. حابة تحكي عن إيه؟"):
            # عرض رسالة المستخدم فوراً
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # 2. إرسال المحادثة كاملة للموديل (عشان يفتكر الكلام)
            with st.chat_message("assistant"):
                # تحويل رسائل Streamlit لتنسيق يفهمه Gemini
                history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"حصل خطأ بسيط: {e}")
else:
    st.warning("رجاءً ضعي المفتاح في صفحة Secrets أولاً باسم API_KEY.")
