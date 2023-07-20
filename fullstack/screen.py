import streamlit as st
import lib.airtable as at
import os
from PyPDF2 import PdfReader
import re
import lib.resume as rs

# st.text()
st.image("./assets/logo.png", width=200)
progress = 0

st.write(
    """
# Fullstack Developer
We are a rapidly growing product studio that builds magical software, helping companies go from 0 to 1 on digital products. You'll work with exceptional peers who’ve left top tech companies to escape the corporate red tape for startup agility.

# **About Beavr Labs:**

At Beavr Labs, we have cultivated a culture that:

- Encourages us to be scrappy, while ensuring we quickly iterate towards perfection.
- Lets us be explorers, employing robust systems to guide our ventures.
- Instills a "yes and..." mentality, fostering a collaborative and innovative workspace.
- Enables us to follow our curiosities, driving constant learning and growth.
- Places utmost importance on taking care of our people, providing a supportive and rewarding environment.
- Champions the spirit of ownership, encouraging accountability and dedication in our work.
- Upholds the essence of craftsmanship, promoting meticulous attention to detail and quality in everything we do.

Having stemmed from big tech environments, we strive to avoid the red tape that can hinder progress and creativity. Instead, we offer a dynamic, fast-paced atmosphere where your input makes an immediate impact.

Learn more about us at [beavrlabs.com](http://beavrlabs.com)

# **Responsibilities:**

- Write high quality, maintainable code in TypeScript.
- Develop and maintain our backend services and databases, particularly with CockroachDB and Prisma.
- Work on frontend development with Tailwind and NextJS, ensuring responsiveness and an excellent user experience.
- Engage with the T3 Stack on a daily basis, making the most of its features to deliver state-of-the-art solutions.
- Collaborate with a dynamic team of designers, engineers, and product managers.
- Own full software development life cycle - from concept to design, testing, release, and support.

# **Qualifications:**

- 3+ years of full-stack software development experience.
- Strong proficiency with the T3 Stack.
- Experience with CockroachDB, Prisma, TypeScript, Tailwind, and NextJS is a nice to have.
- Ability to write clean and efficient code, with an eye for detail and optimization.
- Strong understanding of web technologies and database systems.
- Proven ability to work in a fast-paced environment, prioritizing multiple tasks.
- Excellent communication skills and a team player mentality.

# What We Offer

- An opportunity to be a part of a dynamic, fast-paced product studio that operates like a startup.
- The chance to work on a variety of projects with different requirements and technologies.
- A work culture that supports and encourages continual learning and growth.
"""
)
st.divider()

st.write(
    """
## Submit Your Application To Beavr Labs
Ready to build **magical** software for fast-growing startups with exceptional peers? Apply Below!
"""
)

name = st.text_input("What's Your Name?")
email = st.text_input("What's Your Email?")
linkedin = st.text_input("Share your LinkedIn URL (optional)")
github = st.text_input("Share your GitHub URL (optional)")
portfolio = st.text_input("Share your Portfolio URL (optional)")
resume = st.file_uploader("Choose a file", type=["pdf"])

clicked = st.button("Submit")


if clicked:
    # validate inputs
    if not name or not email or not resume:
        st.error("Please fill out all required fields")

    # validate email
    if (
        re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email)
        is None
    ):
        st.error("Please enter a valid email address")

    processing = st.info(
        "Processing your application, please do not leave this page..."
    )

    reader = PdfReader(resume)
    number_of_pages = len(reader.pages)
    resume = ""
    for page in reader.pages:
        resume += page.extract_text()

    progress = 30

    # validate resume
    approve, reason = rs.get_rating(resume)

    progress = 100

    processing.empty()
    # print(approve, reason)
    if approve:
        st.success("Your application has been approved!")
        st.info(reason)

    else:
        st.error("Your application has been rejected")
        st.info(reason)
