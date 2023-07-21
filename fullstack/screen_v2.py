import streamlit as st
import lib.airtable as at
import os
from PyPDF2 import PdfReader
import re
import lib.resume as rs
import lib.github as gh
import lib.constants as constants
import lib.airtable as at
import lib.coderbyte as cb
import time
import threading


st.write(st.session_state)

# st.image("./assets/logo.png", width=200)
# st.write(constants.JOB_DESCRIPTION)
# st.divider()
# st.write(
#     """
# ## Submit Your Application To Beavr Labs
# Ready to build **magical** software for fast-growing startups with exceptional peers? Apply Below!
# """
# )


# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "success" not in st.session_state:
    st.session_state.success = False


def long_task():
    print("starting long task")
    time.sleep(5)
    print("done task")


def reset_state():
    st.session_state.disabled = False
    st.session_state.success = True


def handle_click():
    st.session_state.disabled = True
    st.session_state.success = False
    name = st.session_state["name"]
    email = st.session_state["email"]
    linkedin = st.session_state["linkedin"]
    github = st.session_state["github"]
    portfolio = st.session_state["portfolio"]
    resume = st.session_state["resume"]

    print("name", name)
    print("email", email)
    print("linkedin", linkedin)
    print("github", github)
    print("portfolio", portfolio)

    thread = threading.Thread(
        target=long_task,
    )
    st.report_thread.add_report_ctx(thread)
    thread.start()


with st.form("application"):
    st.text_input("What's Your Name?", key="name")
    st.text_input("What's Your Email?", key="email")
    st.text_input("Share your LinkedIn URL (optional)", key="linkedin")
    st.text_input("Share your GitHub URL (optional)", key="github")
    st.text_input("Share your Portfolio URL (optional)", key="portfolio")
    st.file_uploader("Choose a file", type=["pdf"], key="resume")
    form_submit_button = st.form_submit_button(
        label="Submit", on_click=handle_click, disabled=st.session_state.disabled
    )


if st.session_state.success:
    st.success("We've received your application, thanks for applying!")
