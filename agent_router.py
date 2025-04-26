from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

class AgentRouter:
    def __init__(self):
        # Use HuggingFace's DistilBERT for text classification and DistilGPT2 for clarification
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.llm = HuggingFacePipeline.from_model_id(
            model_id="distilgpt2",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 100}
        )

    def classify_query(self, text, has_image):
        # Prioritize image presence for routing to Issue Detection Agent
        if has_image:
            return "issue_detection"
        
        # Keyword-based classification for tenancy FAQs
        faq_keywords = ["landlord", "tenant", "evict", "notice", "rent", "deposit", "lease", "agreement"]
        issue_keywords = ["wall", "damage", "mold", "crack", "leak", "property", "issue", "fix", "repair"]

        text_lower = text.lower()
        # Check for tenancy FAQ keywords
        if any(keyword in text_lower for keyword in faq_keywords):
            return "tenancy_faq"
        # Check for issue-related keywords
        if any(keyword in text_lower for keyword in issue_keywords):
            return "issue_detection"
        
        # Fallback: Use DistilBERT to classify ambiguous text
        result = self.classifier(text)
        if result[0]["label"] == "POSITIVE" and result[0]["score"] > 0.7:
            return "tenancy_faq"
        
        # Fallback: Ask for clarification
        prompt = PromptTemplate(
            input_variables=["text"],
            template="The query '{text}' is unclear. Please clarify if you're asking about a property issue (e.g., damage, repairs) or a tenancy question (e.g., landlord issues, rent)."
        )
        clarification = self.llm(prompt.format(text=text))
        return clarification

    def route(self, text, image=None):
        # Ensure image is treated as present if not None or empty
        has_image = image is not None and os.path.exists(image) if image else False
        agent_type = self.classify_query(text, has_image)
        return agent_type, image