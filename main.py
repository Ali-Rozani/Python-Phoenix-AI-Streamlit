import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

st.title("Phoenix AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_chatbot_response(user_input):
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="You Are A AI Chatbot Who Helps The User & Interacts With The User"),
        SystemMessage(content="Please Explain The Response To The User Vividly"),
        *st.session_state.chat_history,
        HumanMessage(content=user_input)
    ])

    prompt = prompt_template.format()
    response = llm.invoke(prompt)

    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response.content))

    prompt_template_chain = ChatPromptTemplate.from_template("You are a helpful assistant. Please respond to: {user_input}")
    chain = LLMChain(llm=llm, prompt=prompt_template_chain)
    response_chain = chain.run({"user_input": user_input})

    return response.content, response_chain

user_input = st.text_input("You: ", key="user_input")

if st.button("Send"):
    if user_input.lower() == "quit":
        st.write("Goodbye!")
    else:
        try:
            response1, response2 = get_chatbot_response(user_input)
            st.write("Conversational Response:")
            st.write(response1)
            st.write("Single-Response:")
            st.write(response2)
        except Exception as e:
            st.error(f"An error occurred: {e}")