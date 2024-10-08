import re
from tools import tools
from prompts import SYSTEM_MESSAGE
from login_service import login
import streamlit as st
import os
from groq import Groq
import ast
import json
from registration_service import create_new_account

model_name = "llama-3.1-70b-versatile"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_the_messages(input):
    msg = []
    if 'messages' not in st.session_state:
        msg = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": input},
        ]
    else:
        msg = st.session_state['messages']
        msg.append({"role": "system", "content": SYSTEM_MESSAGE})
        msg.append({"role": "user", "content": input})

    st.session_state['messages'] = msg

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
    print("update_chat_history", result)
    chat_history = st.session_state['chat_history']
    chat_history.extend(["", result])


def send_result_login_back_to_model(tool_called):
    args = ast.literal_eval(tool_called.function.arguments)
    username = args['username']
    password = args['password']

    function_call_result_message = {
        "role": "tool",
        "content": json.dumps({
            "username": username,
            "password": password
        }),
        "tool_call_id": tool_called.id
    }
    mesg = st.session_state['messages']
    mesg.append(function_call_result_message)

    completion_payload = {
        "model": model_name,
        "messages": mesg
    }
    response = client.chat.completions.create(
        model=completion_payload["model"],
        messages=completion_payload["messages"]
    )

    return response


def send_result_registration_back_to_model(tool_called):
    args = ast.literal_eval(tool_called.function.arguments)
    username = args['username']
    first_name = args["first_name"]
    last_name = args["last_name"]
    email = args["email"]
    phone_number = args["phone_number"]
    home_address = args["home_address"]
    password = args["password"]

    function_call_result_message = {
        "role": "tool",
        "content": json.dumps({
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "home_address": home_address,
            "password": password
        }),
        "tool_call_id": tool_called.id
    }
    mesg = st.session_state['messages']
    mesg.append(function_call_result_message)

    completion_payload = {
        "model": model_name,
        "messages": mesg
    }
    response = client.chat.completions.create(
        model=completion_payload["model"],
        messages=completion_payload["messages"]
    )
    print("send_result_registration_back_to_model", response)
    return response


def reset_messages():
    print("reset_messages")
    msg = []
    if 'messages' not in st.session_state:
        msg = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": input},
        ]
    st.session_state['messages'] = msg


def update_messages(response):
    msg = st.session_state['messages']
    msg.append({"role": "assistant", "content": response})


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
            update_messages(response.choices[0].message.content)
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            print(tool_call)
            if tool_call:
                service_name = tool_call.function.name
                arguments = ast.literal_eval(tool_call.function.arguments)

                if tool_call.function.name == "user_authentication":
                    result = login(arguments)
                    if re.search('Error', result):
                        update_chat_history(result)
                    else:
                        print("result", result)
                        resp = send_result_login_back_to_model(tool_call)
                        update_chat_history(result)
                else:
                    result = create_new_account(arguments)
                    if re.search('Error', result):
                        update_chat_history(result)
                    else:
                        print("sending result")
                        resp = send_result_registration_back_to_model(tool_call)
                        update_chat_history(result)

                    reset_messages()

    except Exception as ex:
        print("Error while calling the model", ex)
        update_chat_history("Error while calling the model. Say hi to try again")

display_chat_history()
