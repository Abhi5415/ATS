import openai
import json
import os
import lib.constants as constants

openai.api_key = os.getenv("STREAMLIT_OPENAI_KEY")


functions = [
    {
        "name": "rate_applicant",
        "description": "approve or reject an applicant based on their resume and portfolio data",
        "parameters": {
            "type": "object",
            "properties": {
                "approve": {
                    "type": "boolean",
                    "description": "whether or not to approve the applicant",
                },
                "reason": {
                    "type": "string",
                    "description": "why the applicant was approved or rejected",
                },
            },
            "required": ["approve"],
        },
    }
]


def get_prompt(resume, job_description):
    return f"""
  This is an applicant:
  {resume}
  
  Are they a good fit for the following job description?
  {job_description}
  
  You should be reasonably confident in your decision, but you don't need to be 100% certain.
  Be selective and only approve applicants that you think are exceptional and top candidates.
  Remember that most people lie or exaggerate their resume, if the resume seems suspect, reject the applicant.

  Use the rate_applicant function to approve or reject the applicant and provide reasoning for your decision.
  """


def get_rating(resume):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "user", "content": get_prompt(resume, constants.JOB_DESCRIPTION)}
        ],
        functions=functions,
    )

    response_message = response["choices"][0]["message"]
    response = json.loads(response_message["function_call"]["arguments"])

    return response["approve"], response["reason"]
