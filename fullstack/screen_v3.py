import asyncio
import streamlit as st
import time

if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "success" not in st.session_state:
    st.session_state.success = False

st.write(st.session_state)


async def long_task():
    print("starting long task")
    await asyncio.sleep(5)  # this simulates a long running task
    print("done task")


async def handle_click():
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

    # Running long task
    await long_task()
    st.session_state.disabled = False
    st.session_state.success = True


with st.form("application"):
    st.text_input("What's Your Name?", key="name")
    st.text_input("What's Your Email?", key="email")
    st.text_input("Share your LinkedIn URL (optional)", key="linkedin")
    st.text_input("Share your GitHub URL (optional)", key="github")
    st.text_input("Share your Portfolio URL (optional)", key="portfolio")
    st.file_uploader("Choose a file", type=["pdf"], key="resume")

    if st.form_submit_button(
        label="Submit", disabled=st.session_state.get("disabled", False)
    ):
        asyncio.run(handle_click())

if st.session_state.success:
    st.success("We've received your application, thanks for applying!")
