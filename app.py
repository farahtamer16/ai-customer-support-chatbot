from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import re
from backend.sentiment_analyzer import SentimentAnalyzer
from backend.intent_recognizer import IntentRecognizer
from backend.faq_matcher import FAQMatcher
from backend.user_profiles import UserProfiles
from context_token_trimmer import trim_memory_to_fit
from translatepy import Translator as TranslatepyTranslator
import requests
import json

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "fallback-secret")

# Initialize backend components
sentiment_analyzer = SentimentAnalyzer()
intent_recognizer = IntentRecognizer()
faq_matcher = FAQMatcher('faq.csv')
user_profiles = UserProfiles()
translator = TranslatepyTranslator()

# Constants
MAX_MEMORY = 10  # How many past chat messages to remember
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = os.getenv("SITE_URL", "http://localhost:5000")
SITE_NAME = os.getenv("SITE_NAME", "AI Customer Support")

# --- Helper Functions ---

def detect_sentiment(text):
    """Analyze user message and return chatbot tone (positive, neutral, empathetic)."""
    result = sentiment_analyzer.analyze(text)
    return sentiment_analyzer.get_response_tone(result)

def get_ai_response(prompt, sentiment="neutral", history=None):
    """Primary function to get a smart AI response via OpenRouter API."""
    try:
        if history is None:
            history = []

        # Adjust bot tone based on detected sentiment
        if sentiment == "frustrated":
            tone_instruction = "Respond calmly, empathetically, and avoid technical jargon."
        elif sentiment == "positive":
            tone_instruction = "Respond in a cheerful, brief, and helpful tone."
        else:
            tone_instruction = "Respond in a professional and helpful tone with clear explanations."

        # Build full message history for API
        system_prompt = f"You are a helpful and professional AI customer support assistant. {tone_instruction}"
        history = trim_memory_to_fit(history, system_prompt, max_tokens=6000)
        full_messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": prompt}]

        # OpenRouter fallback models if one fails (rate limits, etc.)
        fallback_models = [
            "deepseek/deepseek-r1-distill-qwen-32b:free",
            "mistralai/mistral-7b-instruct:free",
            "huggingfaceh4/zephyr-7b-beta:free",
            "openchat/openchat-3.5-0106:free",
            "meta-llama/llama-2-7b-chat:free",
            "tiiuae/falcon-7b-instruct:free",
            "nousresearch/nous-hermes2:free"
        ]

        for model in fallback_models:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": SITE_URL,
                    "X-Title": SITE_NAME,
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": model,
                    "messages": full_messages
                })
            )

            data = response.json()
            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"]

            error_info = data.get("error", {})
            if isinstance(error_info, dict) and error_info.get("code") == 429:
                continue  # Try next model if rate limit error

        return None  # No model succeeded

    except Exception as e:
        return None

# --- Flask Routes ---

@app.route("/")
def home():
    """Serve the homepage with the chat interface."""
    return render_template("index.html")

@app.route("/set_language", methods=["POST"])
def set_language():
    """Allow user to set preferred language for conversation."""
    data = request.get_json()
    lang = data.get("language", "en")
    session["lang"] = lang
    return jsonify({"status": "success", "language": lang})

@app.route("/get", methods=["POST"])
def chatbot_response():
    """Main route: handle user message, detect sentiment/intent, generate response."""
    data = request.get_json()
    user_message = data.get("message", "")
    user_lang = session.get("lang", "en")

    # Translate user message to English if necessary
    original_message = user_message
    if user_lang != "en":
        try:
            user_message = translator.translate(user_message, "English").result
        except:
            user_message = original_message

    # Detect user sentiment and intent
    sentiment = detect_sentiment(user_message)
    intent = intent_recognizer.detect_intent(user_message)

    # Retrieve user's chat history (memory)
    memory = session.get("chat_history", [])
    memory.append({"role": "user", "content": user_message})
    memory = memory[-MAX_MEMORY:]  # Keep memory size manageable
    session["chat_history"] = memory

    # --- Primary response: Try OpenRouter smart AI first ---
    bot_response = get_ai_response(user_message, sentiment, memory)

    # --- Fallback: Use FAQ matcher if OpenRouter fails ---
    if not bot_response:
        answer, topic = faq_matcher.get_best_match_with_topic(user_message)
        if answer:
            bot_response = answer
        else:
            bot_response = "I'm sorry, I couldn't find an answer. Please contact our support team."

    # Translate bot response back to user's preferred language if needed
    if user_lang != "en":
        try:
            bot_response = translator.translate(bot_response, user_lang).result
        except:
            bot_response = f"(English only): {bot_response}"

    # Update chat memory with bot's response
    memory.append({"role": "assistant", "content": bot_response})
    session["chat_history"] = memory[-MAX_MEMORY:]

    # Send back the response to the frontend
    return jsonify({"response": bot_response})

# --- Run the Flask app ---
if __name__ == "__main__":
    app.run(debug=True)
