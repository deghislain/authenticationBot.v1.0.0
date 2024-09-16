import streamlit as st
from cv2 import VideoCapture, imwrite
from UserManagmentSys.User import User
import uuid
import utilities as util
import requests
import json

create_microservice_url = "http://127.0.0.1:8080/create"
username_microservice_url = "http://127.0.0.1:8080/username"

MISSING_REQUIRED_INFO = "Error: Some required information are missing. Say hi to restart"
SUCCESSFUL_MSG = "Congratulation for the creation of your new account. Say hi to start a new conversation"
REGISTRATION_ERROR_MSG = "Error during the registration process. Please, try again later. Say hi to restart"


def capture_user_picture():
    try:
        cam = VideoCapture(0)
        result, image = cam.read()
        if result:
            username = st.session_state['username']
            imwrite(f"UserManagmentSys/images/{username}.png", image)
            return True
        else:
            return False
    except Exception as ex:
        chat_history = st.session_state['chat_history']
        chat_history.extend([input, "Error while capturing your image. Please ensure that your camera is activated,"
                                    "and that you are looking directly at it before attempting again. Say hi to restart"])
        print("Error while capturing your image", ex)


def store_user(user):
    json_user = json.dumps(user.__dict__)
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    result = requests.post(create_microservice_url, json_user, headers=newHeaders)
    return result


def create_new_account(arguments):
    print("create_new_account START")
    print(arguments)
    username = arguments["username"]
    st.session_state['username'] = username
    first_name = arguments["first_name"]
    last_name = arguments["last_name"]
    email = arguments["email"]
    phone_number = arguments["phone_number"]
    home_address = arguments["home_address"]
    password = arguments["password"]

    if username and password and first_name and last_name and email and phone_number and home_address:
        hash_password = util.hash_password(password)
        user_id = uuid.uuid4()
        user = User(str(user_id), username, hash_password, first_name, last_name, email, phone_number, home_address)
        try:
            if capture_user_picture() and store_user(user).status_code == 200:
                return SUCCESSFUL_MSG
            else:
                return REGISTRATION_ERROR_MSG
        except Exception as ex:
            print("Error during the registration process")
            return REGISTRATION_ERROR_MSG
    else:
        return MISSING_REQUIRED_INFO
