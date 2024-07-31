import os
import streamlit as st
from io import StringIO
import re
import sys
from utils.chatbot.chat_history import ChatHistory
from utils.chatbot.utils import Utilities
from googletrans import Translator, LANGUAGES
from langdetect import detect


from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide", page_icon="💬", page_title="Finsmart | Chat-Bot 🤖")

st.title("Finsmart | Chat-Bot 🤖")

user_api_key = os.getenv("OPENAI_API_KEY")

utils = Utilities()

   

uploaded_file = utils.handle_upload(["pdf", "txt", "csv"])

def translate_text(text, target_lang='en'):
    translator = Translator
    translation = translator.translate(text, dest=target_lang)
    return translation.text


if uploaded_file:

    utils.show_options()

    # Initialize chat history
    history = ChatHistory()
    try:
        chatbot = utils.setup_chatbot(
            uploaded_file, st.session_state["model"], st.session_state["temperature"]
        )
        st.session_state["chatbot"] = chatbot

        if st.session_state["ready"]:
            # Create containers for chat responses and user prompts
            response_container, prompt_container = st.container(), st.container()

            with prompt_container:
                # Display the prompt form
                is_ready, user_input = utils.prompt_form()
                original_language = detect(user_input)
                user_input = translate_text(user_input, 'en')

                # Initialize the chat history
                history.initialize(uploaded_file)

                # Reset the chat history if button clicked
                if st.session_state["reset_chat"]:
                    history.reset(uploaded_file)

                if is_ready:
                    # Update the chat history and display the chat messages
                    history.append("user", user_input)

                    old_stdout = sys.stdout
                    sys.stdout = captured_output = StringIO()

                    output = st.session_state["chatbot"].conversational_chat(user_input)

                    sys.stdout = old_stdout

                    history.append("assistant", output)

                    # Clean up the agent's thoughts to remove unwanted characters
                    thoughts = captured_output.getvalue()
                    cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                    cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)
                    cleaned_thoughts = translate_text(cleaned_thoughts, LANGUAGES[original_language])


                    # Display the agent's thoughts
                    with st.expander("Display the agent's thoughts"):
                        st.write(cleaned_thoughts)

            history.generate_messages(response_container)
    except Exception as e:
        st.error(f"Error: {str(e)}")
