import joblib
import re

# تحميل النموذج
model = joblib.load("model_pipeline.pkl")

# دالة تنظيف النصوص (نفس التي في التدريب)
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'[^ء-يa-zA-Z\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'(.)\1+', r'\1\1', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# قائمة النصوص للاختبار
texts = [
    "هذا إعلان يحتوي على كلمات ممنوعة",
    "مرحبا بك في منصتنا التعليمية الجديدة",
    "اشتري الآن سلاح ناري بسعر مغري",
    "صور بنات نار وفيديوهات +18",
    "بيع سيارة نيسان 2017 نظيفة جدا",
    "عندي تبغ فاخر بدون جمارك",
]

# فحص النصوص
for text in texts:
    cleaned = clean_text(text)
    prediction = model.predict([cleaned])[0]
    print(f"\n📌 النص الأصلي: {text}\n🧽 النص المنظف: {cleaned}\n➡️ التصنيف: {prediction}")
