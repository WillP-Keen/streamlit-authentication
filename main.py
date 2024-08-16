import streamlit as st
import streamlit_authenticator as stauth
from streamlit.source_util import _on_pages_changed, get_pages
import json
from pymongo import MongoClient

from pathlib import Path

import yaml
from yaml.loader import SafeLoader

client = MongoClient(st.secrets["MONGODB_CONNECTION_STRING"])

db = client["will"]
users_collection = db["UserAuthentication"]


def get_users(collection):
    users = {}
    for user in collection.find():
        users[user["user"]] = {"name": user["user"], "password": user["password"]}
    return users


def login_user(username, password):
    user = users_collection.find_one({"user": username})
    if user and user["password"] == password:
        return True
    else:
        return False


def get_credentials():
    credentials = {"usernames": {}}
    for user in users_collection.find():
        credentials["usernames"][user["user"]] = {
            "name": user["user"],
            "password": user["password"],
        }
    return credentials


def authenticate():
    credentials = get_credentials()

    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name="mykeen-auth-cookie",
        cookie_key="mykeen123321neekym",
        cookie_expiry_days=10,
    )

    authenticator.login()

    if st.session_state["authentication_status"]:
        st.success("welcome")

    elif st.session_state["authentication_status"] is False:
        st.error("Username/Password Incorrect")

    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter username and password")


authenticate()
