# /testing/test_intent_recognition.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.intent_recognizer import IntentRecognizer
import pandas as pd

# Initialize intent recognizer
intent_recognizer = IntentRecognizer()

# Test Queries
test_queries = [
    "I want a refund for my last order",
    "Can I get my money back please",
    "I need to return this item",
    "How can I ask for a refund?",
    "Give me a refund immediately",
    "Refund my purchase",
    "I need a refund ASAP",
    "Where do I request a refund?",
    "The product was wrong, refund me",
    "I was overcharged, refund please",
    "I forgot my password",
    "I can't log into my account",
    "I need help resetting my password",
    "Password reset not working",
    "I can't remember my login credentials",
    "How do I reset my password?",
    "Forgot my login password",
    "Can't sign in to the app",
    "Trouble logging in",
    "Lost my password",
    "Where is my order?",
    "Track my order please",
    "Can you check my shipment?",
    "Track my package",
    "What's the status of my order?",
    "When will my order arrive?",
    "Order tracking information please",
    "Where is my package?",
    "Help me track my delivery",
    "Check my order status",
    "Cancel my subscription please",
    "Cancel my order now",
    "I want to unsubscribe",
    "Cancel this service",
    "How do I cancel?",
    "Stop my subscription immediately",
    "Cancel my membership",
    "End my account subscription",
    "Cancel the order I made",
    "I changed my mind, cancel it",
    "Thank you so much!",
    "Thanks a lot for your help",
    "Appreciate the quick response!",
    "I’m grateful for the support",
    "Thanks for the information",
    "Thank you for your assistance",
    "Many thanks",
    "Thank you very much!",
    "Really appreciate it",
    "Thank you for resolving this",
    "How do I update my email address?",
    "Help me change my account settings",
    "How can I edit my profile?",
    "Guide me on how to reset my password",
    "How do I change my payment method?",
    "How to delete my account?",
    "What should I do to recover my account?",
    "Can you help me with setting up my account?",
    "Instructions to update billing info?",
    "I need help with password recovery",
    "There’s a billing issue with my card",
    "I was charged twice",
    "Payment failed during checkout",
    "There's a problem with my invoice",
    "Credit card was declined",
    "Incorrect amount charged",
    "Help with billing error",
    "I paid but order not confirmed",
    "Payment not processed",
    "Issue with subscription billing",
    "My app keeps crashing",
    "I'm getting a system error",
    "The app froze on the login page",
    "Error message popping up",
    "Your website crashed",
    "The app is very buggy",
    "I found a glitch",
    "The update broke the app",
    "Major crash when opening app",
    "Serious technical issues happening",
    "I need to update my profile info",
    "How do I change my username?",
    "Update my account details",
    "Change my email address",
    "I want to update my settings",
    "Modify my account information",
    "Update billing address",
    "Change my contact information",
    "Need to update my password",
    "How can I edit my profile picture?",
    "hi",
    "hello",
    "what's up?",
    "good morning",
    "i need some help",
    "can you assist me?",
    "help",
    "i have a question",
    "what can you do?",
    "can you help me?"
]

# Expected Intents
expected_intents = [
    "request_refund", "request_refund", "request_refund", "request_refund", "request_refund",
    "request_refund", "request_refund", "request_refund", "request_refund", "request_refund",
    "login_issue", "login_issue", "login_issue", "login_issue", "login_issue",
    "login_issue", "login_issue", "login_issue", "login_issue", "login_issue",
    "track_order", "track_order", "track_order", "track_order", "track_order",
    "track_order", "track_order", "track_order", "track_order", "track_order",
    "cancel_request", "cancel_request", "cancel_request", "cancel_request", "cancel_request",
    "cancel_request", "cancel_request", "cancel_request", "cancel_request", "cancel_request",
    "gratitude", "gratitude", "gratitude", "gratitude", "gratitude",
    "gratitude", "gratitude", "gratitude", "gratitude", "gratitude",
    "guidance_request", "guidance_request", "guidance_request", "guidance_request", "guidance_request",
    "guidance_request", "guidance_request", "guidance_request", "guidance_request", "guidance_request",
    "payment_issue", "payment_issue", "payment_issue", "payment_issue", "payment_issue",
    "payment_issue", "payment_issue", "payment_issue", "payment_issue", "payment_issue",
    "bug_report", "bug_report", "bug_report", "bug_report", "bug_report",
    "bug_report", "bug_report", "bug_report", "bug_report", "bug_report",
    "account_update", "account_update", "account_update", "account_update", "account_update",
    "account_update", "account_update", "account_update", "account_update", "account_update",
    "general_inquiry", "general_inquiry", "general_inquiry", "general_inquiry", "general_inquiry",
    "general_inquiry", "general_inquiry", "general_inquiry", "general_inquiry", "general_inquiry"
]

# Results list
results = []

for query, expected in zip(test_queries, expected_intents):
    detected = intent_recognizer.detect_intent(query)
    results.append({
        "Query": query,
        "Expected Intent": expected,
        "Detected Intent": detected,
        "Match": "✅" if expected == detected else "❌"
    })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("intent_test_results.csv", index=False)

# Calculate and print overall accuracy
total_tests = len(results)
correct_matches = sum(1 for r in results if r["Match"] == "✅")
accuracy = (correct_matches / total_tests) * 100

print("Intent recognition test completed. Results saved to 'intent_test_results.csv'")
print(f"Total Queries Tested: {total_tests}")
print(f"Correct Matches: {correct_matches}")
print(f"Intent Detection Accuracy: {accuracy:.2f}%")
