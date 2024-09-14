from tools import tools
from prompts import SYSTEM_MESSAGE
from login_service import login
import streamlit as st
import os
from groq import Groq
import ast

model_name = "llama-3.1-70b-versatile"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_the_messages(input):
    msg = []
    if 'messages' not in st.session_state:
        msg = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {
                "role": "user",
                "content": input,
            },
        ]
        st.session_state['messages'] = msg
    else:
        msg = st.session_state['messages']
        msg.append({"role": "system",
                    "content": SYSTEM_MESSAGE})
        msg.append({"role": "user", "content": input})

    return msg


def display_chat_history():
    if 'chat_history' in st.session_state:
        chat_history = st.session_state['chat_history']
        count = 0
        for m in chat_history:
            if m != "":
                if count % 2 == 0:
                    output = st.chat_message("user")
                    output.write(m)
                else:
                    output = st.chat_message("assistant")
                    output.write(m)
            count += 1


def store_chat_history(input, response):
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    chat_history = st.session_state['chat_history']
    chat_history.extend([input, response])


def update_chat_history(result):
    chat_history = st.session_state['chat_history']
    chat_history.extend(["", result])


input = st.chat_input("Say hi to start a new conversation")
if input:
    result = ""
    try:
        messages = get_the_messages(input)
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            tool_choice="auto",  # Let the LLM decide if it should use one of the available tools
            max_tokens=4096,
        )
        if response.choices[0].message.content:
            store_chat_history(input, response.choices[0].message.content)
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            if tool_call:
                service_name = tool_call.function.name
                arguments = ast.literal_eval(tool_call.function.arguments)

                if tool_call.function.name == "user_authentication":
                    result = login(arguments)
                    update_chat_history(result)

    except Exception as ex:
        print("Error while calling the model", ex)
        update_chat_history(result)

display_chat_history()
