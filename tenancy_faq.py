from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

class TenancyFAQAgent:
    def __init__(self):
        self.llm = HuggingFacePipeline.from_model_id(
            model_id="distilgpt2",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 150}
        )

    def answer(self, text):
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Answer the tenancy-related question: '{text}'.\nIf location-specific information is needed, ask the user to provide their city or region."
        )
        response = self.llm(prompt.format(text=text))
        return response