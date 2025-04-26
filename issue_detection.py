from clarifai.client.model import Model
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

class IssueDetectionAgent:
    def __init__(self):
        self.llm = HuggingFacePipeline.from_model_id(
            model_id="distilgpt2",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 150}
        )
        # Get Clarifai PAT from environment
        self.clarifai_pat = os.getenv("CLARIFAI_PAT")
        if not self.clarifai_pat:
            raise ValueError("CLARIFAI_PAT not found in .env")

    def analyze_image(self, image_path):
        try:
            # Use Clarifai's general model for image tagging with PAT
            model = Model(
                "https://clarifai.com/clarifai/main/models/general-image-recognition",
                pat=self.clarifai_pat
            )
            response = model.predict_by_filepath(image_path, input_type="image")
            
            # Extract labels/concepts from Clarifai response
            labels = [concept.name.lower() for concept in response.outputs[0].data.concepts]
            issues = []
            if "mold" in labels or "fungus" in labels:
                issues.append("Mold growth detected, possibly due to high humidity or a leak.")
            if "crack" in labels or "fracture" in labels:
                issues.append("Cracks detected, may indicate structural issues.")
            if "water" in labels or "stain" in labels or "wet" in labels:
                issues.append("Water damage or stains detected.")
            if not issues:
                issues.append("No clear issues detected.")
            return issues
        except Exception as e:
            return [f"Error analyzing image: {str(e)}"]

    def troubleshoot(self, text, image_path):
        issues = self.analyze_image(image_path) if image_path else ["No image provided."]
        prompt = PromptTemplate(
            input_variables=["text", "issues"],
            template="User asked: '{text}'\nDetected issues: {issues}\nProvide troubleshooting suggestions."
        )
        response = self.llm(prompt.format(text=text, issues=issues))
        return response