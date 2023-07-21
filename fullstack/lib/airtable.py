import os
from pyairtable import Table

table = Table(
    os.getenv("STREAMLIT_AIRTABLE"), "appXv9KUtH4yFNcNT", "Fullstack Applicants"
)


def create_applicant(name, email, linkedin, github, portfolio, resume, approve, notes):
    try:
        table.create(
            {
                "Email": email,
                "Name": name,
                "Linkedin": linkedin,
                "Github": github,
                "Portfolio": portfolio,
                "Resume": resume,
                "Status": "Online Assessment" if approve else "Screen",
                "In Consideration": approve,
                "Screen Notes": notes,
            }
        )

        return False, "Successfully saved your application"
    except Exception as e:
        print(e)
        return (
            True,
            "Failed to save your application, you may have already applied, check your email for a confirmation",
        )
