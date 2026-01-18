import os
from groq import Groq
from dotenv import load_dotenv
from ai.chatbot_prompt import build_chatbot_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_chatbot_response(financials, metrics, user_question, chat_history):
    """
    Generates a conversational AI response using:
    - Financial context
    - Business metrics
    - Previous chat history (for follow-up questions)
    """

    # Build the main prompt (business context + metrics + user question)
    prompt = build_chatbot_prompt(financials, metrics, user_question)

    messages = []

    # Add previous chat history for conversational context
    for msg in chat_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add current prompt as the latest user message
    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    return response.choices[0].message.content.strip()
