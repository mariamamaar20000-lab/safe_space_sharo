import google.generativeai as genai

# حط المفتاح بتاعك هنا
genai.configure(api_key="AIzaSyDrvwbLS9l4_j0DkfsTmujF6E0e9Ki4E9Q")

# إعداد التعليمات البرمجية (ده اللي بيخلي طريقتي نفسية وهادية)
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # التعليمات اللي بتحدد شخصيتي
  system_instruction="أنت خبير في علم النفس، تتحدث بلهجة هادئة، داعمة، وذكية مثل Gemini. وظيفتك هي تقديم معلومات نفسية دقيقة بأسلوب بسيط ومريح للمستخدم. لا تعطي نصائح طبية نهائية بل قدم استشارات توعوية.",
)

# ابدأ المحادثة
chat_session = model.start_chat(history=[])

response = chat_session.send_message("أهلاً، أنا محتاج أعرف معلومات عن القلق النفسي")
print(response.text)
