import streamlit as st
from agent_router import AgentRouter
from issue_detection import IssueDetectionAgent
from tenancy_faq import TenancyFAQAgent
import os

st.title("Multi-Agent Real Estate Chatbot")

# Initialize agents
router = AgentRouter()
issue_agent = IssueDetectionAgent()
faq_agent = TenancyFAQAgent()

# User input
user_text = st.text_input("Ask a question or describe an issue:")
uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "png"])

if st.button("Submit"):
    image_path = None
    if uploaded_image:
        image_path = f"temp_{uploaded_image.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

    # Route the query
    agent_type, image = router.route(user_text, image_path)

    # Process based on agent type
    if agent_type == "issue_detection":
        response = issue_agent.troubleshoot(user_text, image_path)
        st.write("**Issue Detection Response:**")
        st.write(response)
        if image_path:
            st.image(image_path, caption="Uploaded Image")
    elif agent_type == "tenancy_faq":
        response = faq_agent.answer(user_text)
        st.write("**Tenancy FAQ Response:**")
        st.write(response)
    else:
        st.write(agent_type)  # Clarification response

    # Clean up
    if image_path and os.path.exists(image_path):
        os.remove(image_path)