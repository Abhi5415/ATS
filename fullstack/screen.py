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

st.write(st.session_state)

# st.text()
st.image("./assets/logo.png", width=200)
gh_error = None

st.write(constants.JOB_DESCRIPTION)
st.divider()
st.write(
    """
## Submit Your Application To Beavr Labs
Ready to build **magical** software for fast-growing startups with exceptional peers? Apply Below!
"""
)


# Disable the submit button after it is clicked
def disable():
    st.session_state.disabled = True


def enable():
    st.session_state.disabled = False


# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False


def handle_click():
    disable()
    name = st.session_state["name"]
    email = st.session_state["email"]
    linkedin = st.session_state["linkedin"]
    github = st.session_state["github"]
    portfolio = st.session_state["portfolio"]
    resume = st.session_state["resume"]

    # validate inputs
    if not name or not email or not resume:
        st.error(
            "Please fill out all required fields, make sure to press enter in every field before submitting"
        )

    # validate email
    if (
        re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email)
        is None
    ):
        st.error("Please enter a valid email address")

    reader = PdfReader(resume)
    resume = ""
    for page in reader.pages:
        resume += page.extract_text()

    github_data = None
    if github:
        github_slug = list(filter(lambda x: x != "", github.split("/")))[-1]
        error, github_data = gh.evaluate_applicant(github_slug)
        if error:
            gh_error = st.error("There was an error processing your GitHub profile")
            return

        print(github_data)

    # validate resume
    approve, reason = rs.get_rating(resume, github_data)
    print(approve, reason)

    at.create_applicant(
        name, email, linkedin, github, portfolio, resume, approve, reason
    )

    if approve:
        error, status = cb.invite_candidate(email)
        if error:
            st.error(
                "There was an error inviting you to the assessment, someone will reach out to you shortly"
            )
            return

    st.success("We've received your application, thanks for applying!")
    enable()


with st.form("application"):
    st.text_input("What's Your Name?", key="name")
    st.text_input("What's Your Email?", key="email")
    st.text_input("Share your LinkedIn URL (optional)", key="linkedin")
    st.text_input("Share your GitHub URL (optional)", key="github")
    st.text_input("Share your Portfolio URL (optional)", key="portfolio")
    st.file_uploader("Choose a file", type=["pdf"], key="resume")
    submit_button = st.form_submit_button(
        label="Submit", on_click=handle_click, disabled=st.session_state.disabled
    )
