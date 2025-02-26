import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-pro")

# Streamlit app title
st.title("AI Chatbot with Google Gemini")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to handle the chatbot response
def get_chatbot_response(user_input):
    # Add user input to chat history
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    # Generate response using Google Gemini
    response = model.generate_content(st.session_state.chat_history)

    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "model", "parts": [response.text]})

    return response.text

# Streamlit input and output
user_input = st.text_input("You: ", key="user_input")

if st.button("Send"):
    if user_input.lower() == "quit":
        st.write("Goodbye!")
    else:
        try:
            response = get_chatbot_response(user_input)
            st.write("AI Response:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display chat history
st.write("Chat History:")
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.write(f"**You:** {message['parts'][0]}")
    elif message["role"] == "model":
        st.write(f"**AI:** {message['parts'][0]}")
