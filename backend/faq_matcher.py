import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FAQMatcher:
    def __init__(self, filepath):
        # Load the FAQ dataset from the provided file
        self.data = pd.read_csv(filepath)
        print(f"✅ Loaded dataset: {filepath}")
        print(f"📄 Total FAQs loaded: {len(self.data)}")
        
        # Extract relevant columns, safely filling missing values
        self.questions = self.data["Customer_Issue"].fillna("").tolist()
        self.answers = self.data["Tech_Response"].fillna("").tolist()
        self.topics = self.data["Topic"].fillna("general").tolist()
        self.follow_up_triggers = self.data.get("Follow_Up_Trigger", [""]).fillna("").tolist()
        self.follow_up_responses = self.data.get("Follow_Up_Response", [""]).fillna("").tolist()
        
        # Create a TF-IDF vectorizer and fit it to the customer questions
        self.vectorizer = TfidfVectorizer().fit(self.questions)
        self.vectors = self.vectorizer.transform(self.questions)

    def get_best_match_with_topic(self, query):
        """Find the most relevant FAQ answer and topic for a given user query."""
        # Transform the user query into TF-IDF vector
        query_vec = self.vectorizer.transform([query])
        
        # Compute cosine similarity between user query and all FAQs
        similarity = cosine_similarity(query_vec, self.vectors)
        
        # Find the FAQ with the highest similarity score
        best_idx = similarity.argmax()
        best_score = similarity[0, best_idx]
        
        # If the similarity is too low, assume no good match was found
        if best_score < 0.5:
            return None, None
        
        # Otherwise, return the best matching answer and its associated topic
        return self.answers[best_idx], self.topics[best_idx]

    def get_follow_up_response_by_topic(self, topic):
        """Find and return a follow-up response based on the detected topic."""
        # Check if the given topic exists in the dataset
        if topic in self.topics:
            idx = self.topics.index(topic)
            
            # If a follow-up response exists for this topic, return it
            if self.follow_up_responses[idx]:
                return self.follow_up_responses[idx]
        
        # If no follow-up response exists, return None
        return None
