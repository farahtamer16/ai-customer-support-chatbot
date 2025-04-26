from typing import Dict, List, Optional
import time

class UserProfiles:
    def __init__(self):
        # Dictionary to store all user profiles: user_id -> profile details
        self.profiles = {}
        # Additional storage dictionary (for saving profiles if needed)
        self.data = {}
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Retrieve a user profile, or create a new one if it doesn't exist."""
        if user_id not in self.profiles:
            # Initialize a new profile structure for new users
            self.profiles[user_id] = {
                "conversation_history": [],
                "sentiment_trends": [],
                "interaction_count": 0,
                "common_issues": {},
                "last_interaction": None
            }
        return self.profiles[user_id]
    
    def add_interaction(self, user_id: str, query: str, response: str, sentiment: Dict[str, float]) -> None:
        """Add a new interaction (query and response) to the user's profile."""
        profile = self.get_user_profile(user_id)
        
        # Create a new interaction record
        interaction = {
            "timestamp": time.time(),
            "query": query,
            "response": response,
            "sentiment": sentiment
        }
        
        # Update profile with new interaction data
        profile["conversation_history"].append(interaction)
        profile["sentiment_trends"].append(sentiment["sentiment"])
        profile["interaction_count"] += 1
        profile["last_interaction"] = time.time()
        
        # Keep only the most recent 10 conversations
        if len(profile["conversation_history"]) > 10:
            profile["conversation_history"] = profile["conversation_history"][-10:]
        
        # Keep only the most recent 20 sentiment records
        if len(profile["sentiment_trends"]) > 20:
            profile["sentiment_trends"] = profile["sentiment_trends"][-20:]
    
    def get_conversation_history(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Retrieve the most recent conversation history for a user (default 5)."""
        profile = self.get_user_profile(user_id)
        return profile["conversation_history"][-limit:]
    
    def get_average_sentiment(self, user_id: str) -> float:
        """Calculate and return the average sentiment score for a user."""
        profile = self.get_user_profile(user_id)
        sentiments = profile["sentiment_trends"]
        
        if not sentiments:
            return 0.0  # No sentiment history yet
        
        return sum(sentiments) / len(sentiments)
    
    def is_returning_user(self, user_id: str) -> bool:
        """Check if the user has interacted more than once."""
        profile = self.get_user_profile(user_id)
        return profile["interaction_count"] > 1
    
    def get_interaction_frequency(self, user_id: str) -> str:
        """Categorize user based on their number of interactions."""
        profile = self.get_user_profile(user_id)
        count = profile["interaction_count"]
        
        if count <= 1:
            return "new_user"
        elif count < 5:
            return "occasional"
        else:
            return "frequent"
        
    def update_topic(self, user_id: str, topic: str) -> None:
        """Set or update the current conversation topic for the user."""
        profile = self.get_user_profile(user_id)
        profile['current_topic'] = topic
        self.save_user_profile(user_id, profile)

    def get_current_topic(self, user_id: str) -> Optional[str]:
        """Retrieve the current conversation topic for the user."""
        profile = self.get_user_profile(user_id)
        return profile.get('current_topic')
    
    def store_entity(self, user_id: str, key: str, value: str) -> None:
        """Store a named entity (like user-provided information) in the profile."""
        profile = self.get_user_profile(user_id)
        entities = profile.get('entities', {})
        entities[key] = value
        profile['entities'] = entities
        self.save_user_profile(user_id, profile)

    def get_entity(self, user_id: str, key: str) -> Optional[str]:
        """Retrieve a previously stored entity value for the user."""
        profile = self.get_user_profile(user_id)
        return profile.get('entities', {}).get(key)
    
    def save_user_profile(self, user_id: str, profile: dict) -> None:
        """Save the updated profile back to the internal data storage."""
        self.data[user_id] = profile

    def update_current_intent(self, user_id: str, intent: str):
        """Set or update the user's current detected intent."""
        profile = self.get_user_profile(user_id)
        profile["current_intent"] = intent

    def get_current_intent(self, user_id: str) -> Optional[str]:
        """Retrieve the user's currently active intent."""
        profile = self.get_user_profile(user_id)
        return profile.get("current_intent")
