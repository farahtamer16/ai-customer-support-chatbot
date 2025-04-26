# /testing/test_sentiment_model.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import pandas as pd

# Load your trained sentiment model
model = joblib.load(os.path.join("backend", "sentiment_model.pkl"))

# Test Samples
samples = [
    "I'm extremely happy with the service", # positive
    "This is absolutely terrible", # negative
    "Could you assist me with the setup?", # neutral
    "Fantastic product, will buy again!", # positive
    "I hate how complicated this is", # negative
    "Okay, let's continue", # neutral
    "Best experience I've ever had", # positive
    "I am so annoyed by this app crashing", # negative
    "What's the next step?", # neutral
    "Thank you for resolving my issue!", # positive
    "This is making me very angry", # negative
    "Can you help me?", # neutral
    "Love the update you released!", # positive
    "I'm fed up with all these bugs", # negative
    "Need instructions please", # neutral
    "The team was very supportive", # positive
    "System error again? Seriously?", # negative
    "When should I expect a reply?", # neutral
    "Really appreciate the quick turnaround", # positive
    "Nothing is working as it should", # negative
    "Thanks for your help!", # positive
    "This situation is beyond frustrating", # negative
    "Just checking if my order is confirmed", # neutral
    "Thrilled with the results!", # positive
    "Deeply disappointed by the service", # negative
    "Can you explain the next steps?", # neutral
    "I absolutely love this feature", # positive
    "Why does it always crash on login?", # negative
    "Just wondering about my status update", # neutral
    "Grateful for the excellent support", # positive
    "Really upset about the delays", # negative
    "Could you please guide me?", # neutral
    "Wonderful customer care!", # positive
    "Another bug? I'm done", # negative
    "Can we proceed to the next phase?", # neutral
    "I'm delighted with the response", # positive
    "Still waiting and very annoyed", # negative
    "What documents are needed?", # neutral
    "Big thanks to the entire support team!", # positive
    "Nothing but issues with this app", # negative
    "Is there anything else needed from me?", # neutral
    "Super pleased with your service!", # positive
    "I'm losing patience here", # negative
    "Could you assist me further?", # neutral
    "Ecstatic about the fast reply!", # positive
    "My problem is still unresolved and it's maddening", # negative
    "Where do I upload the files?", # neutral
    "Very impressed by your responsiveness", # positive
    "The system is unusable right now", # negative
    "Any update on my ticket?", # neutral
    "Appreciate your time and effort", # positive
    "Very angry with the constant failures", # negative
    "Just following up", # neutral
    "Amazing work on the new version", # positive
    "Facing many glitches still", # negative
    "What are the next instructions?", # neutral
    "You saved my day!", # positive
    "Terrible experience, very disappointing", # negative
    "Looking forward to hearing from you", # neutral
    "Awesome support experience", # positive
    "Extremely dissatisfied with the service", # negative
    "How long does verification take?", # neutral
    "You’ve been very helpful, thanks!", # positive
    "I keep encountering errors", # negative
    "Could you point me to the right link?", # neutral
    "Super smooth setup, thank you!", # positive
    "Crashing non-stop again", # negative
    "Just wanted to clarify something", # neutral
    "Fabulous customer experience", # positive
    "Very disappointed today", # negative
    "Should I expect a confirmation email?", # neutral
    "Everything worked perfectly!", # positive
    "Not satisfied at all", # negative
    "Requesting a quick check on my case", # neutral
    "Loved the way you handled it!", # positive
    "Terrible first impression", # negative
    "What’s the processing time?", # neutral
    "Can't thank you enough", # positive
    "Beyond annoyed with the delays", # negative
    "Could you review my application?", # neutral
    "Flawless delivery!", # positive
    "This app is a disaster", # negative
    "Is there a form I need to fill?", # neutral
    "I'm grateful for your patience", # positive
    "Still no fix, very angry", # negative
    "Checking on my appointment", # neutral
    "Brilliant assistance!", # positive
    "Angry about the repeated mistakes", # negative
    "Can I resubmit the documents?", # neutral
]

expected_sentiments = [
    "positive", "negative", "neutral", "positive", "negative", "neutral",
    "positive", "negative", "neutral", "positive", "negative", "neutral",
    "positive", "negative", "neutral", "positive", "negative", "neutral",
    "positive", "negative", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral", "positive",
    "negative", "neutral", "positive", "negative", "neutral"
]


# Run model prediction for each
results = []

for s, expected in zip(samples, expected_sentiments):
    pred = model.predict([s])[0]
    match = "✅" if pred == expected else "❌"
    results.append({
        "Sentence": s,
        "Expected Sentiment": expected,
        "Predicted Sentiment": pred,
        "Match": match
    })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("test_sentiment_model.csv", index=False)

# Calculate and print statistics
total_tests = len(results)
correct_matches = sum(1 for r in results if r["Match"] == "✅")
accuracy = (correct_matches / total_tests) * 100

# Count positive/negative/neutral breakdown
predicted_positive = sum(1 for r in results if r["Predicted Sentiment"] == "positive")
predicted_negative = sum(1 for r in results if r["Predicted Sentiment"] == "negative")
predicted_neutral = sum(1 for r in results if r["Predicted Sentiment"] == "neutral")

print("Sentiment detection structured test completed. Results saved to 'test_sentiment_model.csv'")
print(f"Total Sentences Tested: {total_tests}")
print(f"Correct Sentiment Matches: {correct_matches}")
print(f"Sentiment Detection Accuracy: {accuracy:.2f}%")
print(f"Positive Sentiments Detected: {predicted_positive}")
print(f"Negative Sentiments Detected: {predicted_negative}")
print(f"Neutral Sentiments Detected: {predicted_neutral}")
