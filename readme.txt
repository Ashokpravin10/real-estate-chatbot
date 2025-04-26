# Multi-Agent Real Estate Chatbot

## Overview
A multi-agent chatbot for real estate, featuring:
- **Agent 1**: Issue Detection (image + text) using Clarifai Community API and Ollama.
- **Agent 2**: Tenancy FAQ (text-based) using Ollama.
- **Agent Router**: Routes queries based on image presence and text keywords.

## Tools Used
- Streamlit: Web UI
- LangChain: Agent logic
- Clarifai Community API: Image analysis (free tier)
- HuggingFace Transformers (Ollama): Text generation
- Deployment: Streamlit Cloud

## Agent Switching Logic
- **Image Present**: Routes to Agent 1 if an image is uploaded.
- **Text Keywords**: Routes to Agent 1 for property keywords (e.g., "wall", "mold") or Agent 2 for tenancy keywords (e.g., "landlord", "rent").
- **Fallback**: Asks for clarification.

## Image-Based Issue Detection
- Clarifai API detects labels (e.g., "mold", "crack") using a Personal Access Token (PAT).
- Ollama generates troubleshooting suggestions.

## Use Case Examples
1. **Issue Detection**:
   - User: "What's wrong with this wall?" (uploads image)
   - Response: "Mold detected. Check for leaks and use a dehumidifier."
2. **Tenancy FAQ**:
   - User: "Can my landlord evict me without notice?"
   - Response: "Landlords must give notice. Provide your city for specifics."

## Steps to View
1. Visit the deployed URL.
2. Enter a question or upload an image and submit.
3. View the response.

## Local Setup
```cmd
git clone [repo-url]
cd real_estate_chatbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
