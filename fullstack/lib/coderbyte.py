import requests
import json
import os
import lib.constants as constants


def invite_candidate(email):
    try:
        print("inviting candidate")
        r = requests.post(
            "https://coderbyte.com/api/organization/candidates/invite",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {os.getenv('STREAMLIT_CODERBYTE_TOKEN')}",
            },
            data=json.dumps(
                {"candidates": [email], "assessment_url": constants.ASSESSMENT_LINK}
            ),
        )

        print(r.status_code, r.text)

        return False, "Successfully invited candidate"
    except Exception as e:
        print(e)
        return True, "Failed to invite candidate"
