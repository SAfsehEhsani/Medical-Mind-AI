import streamlit as st
from llm_service import get_medical_insight # Import the function from your module

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="AI DiagnoXpert",
    page_icon="⚕️",
    layout="wide"
)

# --- Header and Disclaimer ---
st.title("⚕️ AI DiagnoXpert - AI Powered Medical Assistant")


st.info("Ask me about general health topics, symptoms (causes & diagnosis), or basic drug information.")

# --- Chat Interface ---

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages in the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input for the user
prompt = st.chat_input("Ask me a health-related question...")

# Process user input when submitted
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare history for LLM call (exclude system message which is added in the service)
    # Only include 'user' and 'assistant' roles for conversation history
    chat_history_for_llm = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages if m["role"] in ["user", "assistant"]
    ]


    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = get_medical_insight(prompt, chat_history_for_llm)
            st.markdown(ai_response) # Use markdown to render potentially formatted text

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Optional: Add a button to clear chat history
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun() # Rerun the app to clear the display
    
st.markdown(                          "Developed By Syed Afseh Ehsani")