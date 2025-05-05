import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
# Ensure the GROQ_API_KEY environment variable is set
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables or .env file")

client = Groq(api_key=groq_api_key)

def get_medical_insight(user_prompt: str, chat_history: list):
    """
    Sends a user prompt and chat history to the Groq API and returns the AI response.

    Args:
        user_prompt (str): The current query from the user.
        chat_history (list): A list of previous messages in the conversation,
                             formatted for the Groq API ([{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]).

    Returns:
        str: The content of the AI's response message. Returns an error message if the API call fails.
    """
    # Define the system message - CRITICAL for guiding the AI's behavior
    system_message = {
        "role": "system",
        "content": (
            "You are AI DiagnoXpert, an AI-powered medical insight and diagnostic assistant. "
            "Your purpose is to provide general information about health topics, symptoms, and drugs based on your training data. "
            "**ABSOLUTELY DO NOT provide medical diagnoses, treatment plans, or specific medical advice.** "
            "Your responses should be informative but always include a clear disclaimer recommending the user consult a qualified healthcare professional for any health concerns. "
            "Explain medical concepts clearly and concisely. Be helpful and empathetic."
            "Structure drug information clearly (e.g., uses, common side effects - extracted from your knowledge, not external search in this MVP)."
            "When discussing symptoms, mention *possible* causes but reiterate that self-diagnosis is not recommended."
        )
    }

    # Prepare the messages for the API call
    # Start with the system message, then add chat history, then the current user message
    messages = [system_message] + chat_history + [{"role": "user", "content": user_prompt}]

    try:
        # Call the Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192" # Or another suitable model like 'llama3-70b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it'
        )

        # Extract the response content
        ai_response = chat_completion.choices[0].message.content

        # Ensure the disclaimer is present, or add a reminder (basic fallback)
        # A better approach is to rely on the strong system message and UI disclaimer
        if "consult a healthcare professional" not in ai_response.lower() and "medical advice" not in ai_response.lower():
             ai_response += "\n\n**Important:** This information is for educational purposes only and does not constitute medical advice. Always consult with a qualified healthcare professional for any health concerns or before making any decisions related to your health or treatment."


        return ai_response

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return (
            "Sorry, I encountered an error trying to get that information. "
            "Please try again later or consult a healthcare professional."
        )
