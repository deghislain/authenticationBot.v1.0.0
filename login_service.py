import cv2
import streamlit as st
from cv2 import VideoCapture
from skimage.metrics import structural_similarity as ssim
import requests
from utilities import hash_password

login_microservice_url = "http://127.0.0.1:8080/login"

IMAGE_ISSUES_MSG = ("Error: You did not pass the image verification process. Please ensure that your camera is activated,"
                    "and that you are looking directly at it then say hi to try again")

CREDENTIALS_ERROR_MSG = "Error: Invalid username or password. Type hi to try again"
AUTHENTICATION_ERROR_MSG = "Error during the authentication process. Please, try again later or type hi to try again"
SUCCESSFUL_MSG = "Authentication successfully completed."


def image_verification(username):
    if 'image_similarity' in st.session_state and st.session_state['image_similarity'] > 0.60:
        return True

    cam = VideoCapture(0)
    result, image = cam.read()
    if result:
        if username:
            local_image = cv2.imread(f"UserManagmentSys/images/{username}.png")
            s = ssim(local_image, image, channel_axis=2)
            print("similarity  ", s)
            if s > 0.60:
                if 'image_similarity' not in st.session_state:
                    st.session_state['image_similarity'] = s
                return True

    return False


def user_authentication(username, password):
    hashed_password = hash_password(password)
    response = requests.get(login_microservice_url,
                            json={'username': f"{username}", 'password': f"{hashed_password}"})
    return response


def login(arguments):
    username = arguments['username']
    password = arguments['password']

    if image_verification(username):
        if username and password:
            try:
                response = user_authentication(username, password)
                if response.status_code == 200:
                    return SUCCESSFUL_MSG
                else:
                    return CREDENTIALS_ERROR_MSG
            except Exception as ex:
                print("An error occurred during your login", ex)
                return AUTHENTICATION_ERROR_MSG
        else:
            return CREDENTIALS_ERROR_MSG
    else:
        return IMAGE_ISSUES_MSG
