# scripts/intent_module.py

def get_intent(user_input):
    user_input = user_input.lower()
    
    if "reset password" in user_input or "forgot password" in user_input:
        return "password_reset"
    elif "not working" in user_input or "error" in user_input:
        return "technical_issue"
    elif "bill" in user_input or "payment" in user_input:
        return "billing"
    elif "speak to agent" in user_input or "human" in user_input:
        return "escalation"
    else:
        return "unknown"

# Quick test
if __name__ == "__main__":
    test_inputs = [
        "I forgot my password",
        "There's an error with my system",
        "Can I speak to a human please?",
        "How much is my last bill?"
    ]
    
    for msg in test_inputs:
        print(f"Input: {msg}\nIntent: {get_intent(msg)}\n")
