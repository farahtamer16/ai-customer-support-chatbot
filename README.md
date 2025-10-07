# AI Customer Support Chatbot

Welcome to the AI Customer Support Assistant project!  
This intelligent chatbot can:
- Detect user sentiment (positive, neutral, empathetic),
- Recognize user intents (e.g., refund requests, login issues, FAQs),
- Adapt its conversational tone,
- Automatically fall back to OpenRouter API for complex queries,
- Support multiple languages via live translation.

---

## How to Run the Project

### 1. Clone the Repository

git clone https://github.com/farahtamer16/ai-customer-support-chatbot.git
cd ai-customer-support-chatbot

### 2. Create and Activate a Virtual Environment

python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up Environment Variables
The project contains a .env file with an OpenRouter key available for use temporarily. You can replace the contents of the file with your own .env file using your own key.

### 5. Run the Flask Application

python app.py

The app will start at:
http://localhost:5000

Open it in your web browser.

### Features Overview
💬 Multi-language support (auto translation)

- Adaptive tone replies (empathetic, positive, neutral)

- Intent recognition for better query understanding

- FAQ matching fallback if OpenRouter fails

- Session management using Flask sessions

- Sentiment trend tracking for future personalization (UserProfiles module)

### Future Improvements
Add persistent database storage for user profiles

Fine-tune transformer-based sentiment models

Implement conversation analytics dashboard

Real-time monitoring for API fallbacks

### Acknowledgments
OpenRouter.ai (for API integration)

Huggingface and Deepseek models (fallback models)

TranslatePy for language translation

Scikit-learn for intent recognition and FAQ matching

Sumit Kumar. (2024). Tech Support Conversations Dataset [Data set]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/9923955


