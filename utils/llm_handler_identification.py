from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
import os

def initialize_llm():
    template = """
    You are an expert in plant identification and botany. Use the following conversation history and human input to provide detailed information and facts about the identified plant.

    Conversation history:
    {chat_history}

    Human: {human_input}
    AI Assistant: """

    prompt = PromptTemplate(input_variables=["chat_history", "human_input"], template=template)

    if "memory" not in st.session_state:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        st.session_state.memory = memory
    else:
        memory = st.session_state.memory

    api_key = os.getenv("CHATGROQ_API_KEY")
    llm = ChatGroq(
        temperature=0.2,
        model_name='Mixtral-8x7b-32768',
        groq_api_key=api_key
    )

    conversation = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)
    return conversation

def get_response_from_llm(human_input):
    if 'llm_chain' not in st.session_state:
        st.session_state.llm_chain = initialize_llm()

    response = st.session_state.llm_chain.predict(human_input=human_input)
    return response
