import time
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# === Load datasets ===
print("Loading datasets...")
try:
    df1 = pd.read_csv("slang_sentiment_dataset.csv")
    df2 = pd.read_csv("emotional_sentiment_dataset.csv")
    df3 = pd.read_csv("full_support_chat_dataset.csv")
except FileNotFoundError:
    print("❌ Dataset files not found. Please ensure they are in the same directory.")
    exit(1)

# === Combine and shuffle ===
print("Combining datasets...")
df_combined = pd.concat([df1, df2, df3], ignore_index=True)
df_combined = df_combined.dropna(subset=["text", "label"])
df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

X = df_combined["text"]
y = df_combined["label"]

# === Split ===
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# === Parameters to sweep ===
sentiment_thresholds = [0.4, 0.5, 0.6]  # Simulated thresholds
memory_window_sizes = [2, 5, 10]         # Simulated memory windows
ngram_ranges = [(1,1), (1,2), (2,2)]      # Different n-gram ranges

# === Results log ===
results = []

print("Starting parameter sweep...")
for threshold in sentiment_thresholds:
    for memory_window in memory_window_sizes:
        for ngram_range in ngram_ranges:
            # Train model with current n-gram setting
            pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(ngram_range=ngram_range, lowercase=True, stop_words="english", max_features=10000)),
                ("clf", LogisticRegression(max_iter=300))
            ])
            pipeline.fit(X_train, y_train)

            # Evaluate performance
            start_time = time.time()
            y_pred = pipeline.predict(X_test)
            end_time = time.time()

            accuracy = accuracy_score(y_test, y_pred) * 100
            avg_response_time = (end_time - start_time) / len(X_test) * 1000  # in milliseconds

            results.append({
                "Sentiment Threshold": threshold,
                "Memory Window Size": memory_window,
                "N-gram Range": str(ngram_range),
                "Accuracy (%)": round(accuracy, 2),
                "Avg Response Time (ms)": round(avg_response_time, 2)
            })

# === Save results ===
df = pd.DataFrame(results)
df.to_csv("parameter_sweep_results.csv", index=False)

print("✅ Sweep completed. Results saved to 'parameter_sweep_results.csv'.")
