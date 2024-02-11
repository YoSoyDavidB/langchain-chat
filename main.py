import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
  load_dotenv()
  # Load the openai API key
  if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
      st.error("Please set your OpenAI API key as an environment variable.")
      exit(1)
  else:
    print("OpenAI API key loaded successfully")


  st.set_page_config(
    page_title='Streamlit App', 
    page_icon='🤖'
  )            


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
       st.session_state.messages = [
            SystemMessage("Yoy are a helpful assistant."),
       ]

    st.header("Your own GPT 🤖")

    with st.sidebar:
        user_input = st.text_input("Enter your text here", key="user_input")

    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()