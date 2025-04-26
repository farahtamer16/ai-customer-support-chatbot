import difflib

class IntentRecognizer:
    def __init__(self):
        # Expanded keywords with more synonyms and short phrases
        self.intent_keywords = {
            "request_refund": [
                "refund", "money back", "return", "get a refund", "refund my purchase", "overcharged", "wrong product"
            ],
            "login_issue": [
                "forgot password", "password reset", "can't login", "cant login", "cannot login", "unable to login",
                "signin problem", "can't sign in", "lost password", "trouble logging in", "login credentials", "reset password"
            ],
            "track_order": [
                "track order", "order status", "where is my order", "track shipment", "track my package",
                "order tracking", "shipment status", "delivery status", "track delivery", "check order status"
            ],
            "cancel_request": [
                "cancel order", "cancel request", "cancel my service", "unsubscribe", "stop subscription", "cancel my subscription",
                "stop service", "cancel membership", "end subscription", "stop my order"
            ],
            "gratitude": [
                "thank you", "thanks", "thx", "appreciate", "much appreciated", "thank u", "tysm", "really appreciate", "grateful", "thankful"
            ],
            "guidance_request": [
                "how do i", "help me", "how can i", "instructions", "guide me", "how to", "what should i do",
                "can you help me", "assist me", "i need some help", "how do you", "what can you do", "support me"
            ],
            "payment_issue": [
                "billing issue", "charged wrongly", "payment failed", "invoice problem", "credit card problem",
                "overcharged", "billing error", "payment not processed", "charged twice", "subscription billing issue"
            ],
            "bug_report": [
                "crash", "bug", "error", "glitch", "app not working", "system error", "technical issue", "freeze", "froze", "app froze",
                "crashing", "crashed", "app freeze", "system crash", "major crash"
            ],
            "account_update": [
                "change email", "update profile", "update account", "change password", "edit profile",
                "modify account", "update billing address", "change username", "edit settings", "update settings", "edit account info"
            ]
        }

    def detect_intent(self, query: str) -> str:
        query = query.lower()

        # Direct keyword matching first
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return intent

        # Fuzzy matching (lower cutoff to 0.5)
        for intent, keywords in self.intent_keywords.items():
            match = difflib.get_close_matches(query, keywords, n=1, cutoff=0.5)
            if match:
                return intent

        # Fallback
        return "general_inquiry"
