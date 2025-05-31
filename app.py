from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os

app = Flask(__name__)

# ✅ إعداد CORS شامل مع تحسينات
cors = CORS(app, resources={
    r"/predict": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# ✅ قائمة الكلمات الممنوعة (محدثة)
banned_keywords = [
    # المخدرات وأسماءها
    "حشيش", "عشب", "شُمة", "كبتاجون", "حبوب مخدرة", "ترامادول", "ترامادول مخدر", "هيروين",
    "كوكايين", "بودرة", "شبو", "زطلة", "بانجو", "ثلج", "ماريجوانا", "مخدرات", "حبوب", 
    "حبوب هلوسة", "حبوب منشطة", "حبوب مخدرة", "مسكن قوي", "مواد مخدرة", "ليريكا", "ميث",
    "ميثامفيتامين", "كودايين", "جرعة", "تعاطي مخدرات", "إدمان", "مخدر",
    
    # السلاح والعنف
    "سلاح", "بندقية", "طبنجة", "رشاش", "مسدس", "ذخيرة", "كلاشينكوف", "قنابل",
    "صواريخ", "عبوة ناسفة", "مطواة", "خنجر", "موس", "قتل", "اغتيال", "تفجير",
    "تهريب سلاح", "ترويع", "عصابة", "اعتداء", "ذبح", "جريمة", "قطع رقبة", "تهديد بالقتل",

    # التبغ والدخان
    "تبغ", "دخان", "سجائر", "شيشة", "معسل", "فيب", "بود نيكوتين", "نكهات فيب",
    "فيب ممنوع", "شيشة مهربة", "دخان مهرب",

    # الإباحية والشتائم
    "صور فاضحة", "صور مثيرة", "صدر", "نهود", "مؤخرة", "إباحية", "جنس", "دعارة", "سكس", 
    "porno", "nude", "xxx", "fuck", "shit", "bastard", "asshole", "screw", "سكسي", "تعري", 
    "دردشة جنسية", "شات جنسي", "18+", "adult only", "onlyfans", "camgirl", "snap for nudes", 
    "sex chat", "sexy", "بنات نار", "فيديوهات +18", "موقع إباحي", "قصص جنسية", 
    "بنات حلوات", "تعال خاص", "دردشة للكبار",

    # شتائم أخرى وكلمات مسيئة
    "يا كلب", "يا حيوان", "تباً لك", "لعنة الله", "يا ابن ال", "قذر", "منحط", "كذاب", 
    "حقير", "بلا شرف", "نذل", "اخرس", "انقلع", "تفو عليك", "حمار", "وسخ", "وسخة", 
    "متخلف", "أبله", "خنزير", "يا تافه",

    # الاحتيال والنصب
    "تزوير", "نصب", "احتيال", "نقود مزورة", "كسب سريع", "اربح الآن", "ربح مضمون",
    "تحويل بنكي مشبوه", "شراء أصوات", "احتيال بنكي", "تلاعب مالي", "قرصنة", "اختراق",
]

# الحقول التي يتم فحصها
FIELDS_TO_CHECK = [
    "title",
    "description",
    "seller_name",
    "category",
]

def clean_text(text):
    text = text.strip().lower()
    words = re.findall(r'[\u0600-\u06FF\u061B-\u061F\u0640]+', text)
    return words

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    try:
        # معالجة طلبات OPTIONS الاستباقية
        if request.method == 'OPTIONS':
            response = jsonify({
                "status": "ok",
                "message": "Preflight request accepted"
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
            return response
        
        # معالجة طلبات POST
        data = request.get_json()
        for field in FIELDS_TO_CHECK:
            content = data.get(field, "")
            if not content.strip():
                continue
            words = clean_text(content)
            for word in words:
                if word in banned_keywords:
                    return jsonify({
                        "result": "ممنوع",
                        "reason": f"كلمة ممنوعة: {word}",
                        "field": field
                    })
        return jsonify({"result": "مسموح"})
    except Exception as e:
        response = jsonify({
            "result": "خطأ",
            "error": str(e)
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

# معالج بعد الطلب لإضافة رؤوس CORS
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ مهم لـ Render
    app.run(host="0.0.0.0", port=port)
