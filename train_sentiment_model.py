import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

# === Load all datasets ===
print("Loading datasets...")
df1 = pd.read_csv("slang_sentiment_dataset.csv")
df2 = pd.read_csv("emotional_sentiment_dataset.csv")
df3 = pd.read_csv("full_support_chat_dataset.csv")

# === Combine and shuffle ===
print("Combining datasets...")
df_combined = pd.concat([df1, df2, df3], ignore_index=True)
df_combined = df_combined.dropna(subset=["text", "label"])
df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

# === Split ===
print("🧪 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    df_combined["text"], df_combined["label"],
    stratify=df_combined["label"], test_size=0.2, random_state=42
)

# === Train model ===
print("Training model...")
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english", max_features=10000)),
    ("clf", LogisticRegression(max_iter=300))
])
pipeline.fit(X_train, y_train)

# === Evaluate ===
print("Model performance:")
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# === Save model ===
print("Saving model to sentiment_model.pkl...")
joblib.dump(pipeline, "sentiment_model.pkl")

print("Done. Your model is ready!")
