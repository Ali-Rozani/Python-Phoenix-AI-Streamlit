import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

# Streamlit app title
st.title("Phoenix AI 🤖")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to handle the chatbot response
def get_chatbot_response(user_input):
    # First script logic (conversational chatbot)
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="You Are Phoenix AI, an intelligent chatbot designed to help users with their queries."),
        SystemMessage(content="Please provide detailed and helpful responses."),
        *st.session_state.chat_history,  # Include chat history
        HumanMessage(content=user_input)
    ])

    # Generate response using the conversational prompt
    prompt = prompt_template.format()
    response = llm.invoke(prompt)

    # Add the user input and AI response to the chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response.content))

    # Second script logic (single-response chatbot)
    prompt_template_chain = ChatPromptTemplate.from_template("You are a helpful assistant. Please respond to: {user_input}")
    chain = LLMChain(llm=llm, prompt=prompt_template_chain)
    response_chain = chain.run({"user_input": user_input})

    return response.content, response_chain

# Streamlit input and output
user_input = st.text_input("You: ", key="user_input")

if st.button("Send"):
    if user_input.lower() == "quit":
        st.write("Goodbye! Thank you for using Phoenix AI.")
    else:
        try:
            response1, response2 = get_chatbot_response(user_input)
            st.write("Phoenix AI:")
            st.write(response1)
            st.write("Quick Response:")
            st.write(response2)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display chat history
st.write("Chat History:")
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.write(f"**You:** {message.content}")
    elif isinstance(message, AIMessage):
        st.write(f"**Phoenix AI:** {message.content}")
