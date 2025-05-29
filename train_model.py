import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# تحميل stopwords
nltk.download('stopwords')
stop_words_arabic = stopwords.words('arabic')

# دالة تنظيف النصوص
def clean_text(text):
    text = str(text).lower()

    # توحيد الألف والهمزات
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)

    # إزالة الرموز الغريبة
    text = re.sub(r'[^ء-يa-zA-Z\s]', ' ', text)
    
    # إزالة الأرقام
    text = re.sub(r'\d+', ' ', text)

    # إزالة تكرار الحروف (مثلاً: ناااار -> نار)
    text = re.sub(r'(.)\1+', r'\1\1', text)

    # إزالة المسافات الزائدة
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# تحميل البيانات
df = pd.read_csv("data.csv")

# تنظيف البيانات
df.dropna(subset=["text", "label"], inplace=True)
df["text"] = df["text"].apply(clean_text)

# فصل الميزات والوسوم
X = df["text"]
y = df["label"]

# تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# إنشاء النموذج
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=7000,
        ngram_range=(1, 2),
        stop_words=stop_words_arabic,
        sublinear_tf=True
    )),
    ("clf", LogisticRegression(class_weight="balanced", max_iter=1000))
])

# تدريب النموذج
pipeline.fit(X_train, y_train)

# تقييم النموذج
y_pred = pipeline.predict(X_test)
print("\n✅ تقرير الأداء:")
print(classification_report(y_test, y_pred))

# حفظ النموذج
joblib.dump(pipeline, "model_pipeline.pkl")
print("\n✅ تم حفظ النموذج في: model_pipeline.pkl")
