import requests
import os

GITHUB_TOKEN = os.getenv("STREAMLIT_GITHUB_TOKEN")
API_URL = "https://api.github.com"


def get_user_info(username):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"{API_URL}/users/{username}", headers=headers)

    if response.status_code != 200:
        # Handle error
        raise Exception(f"Error fetching user info: {response.status_code}")

    return response.json()


def get_repos(username):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"{API_URL}/users/{username}/repos", headers=headers)

    if response.status_code != 200:
        # Handle error
        raise Exception(f"Error fetching repos: {response.status_code}")

    return response.json()


def get_languages_for_repo(username, repo):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(
        f"{API_URL}/repos/{username}/{repo}/languages", headers=headers
    )

    if response.status_code != 200:
        # Handle error
        raise Exception(f"Error fetching repo languages: {response.status_code}")

    return response.json().keys()


def get_commits_for_repo(username, repo):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(
        f"{API_URL}/repos/{username}/{repo}/commits", headers=headers
    )

    if response.status_code != 200:
        # Handle error
        raise Exception(f"Error fetching repo commits: {response.status_code}")

    return response.json()


def evaluate_applicant(username):
    user_info = get_user_info(username)
    repos = get_repos(username)

    total_stars = 0
    total_commits = 0
    total_repos = len(repos)
    languages = set()

    for repo in repos:
        total_stars += repo["stargazers_count"]
        languages.update(get_languages_for_repo(username, repo["name"]))
        total_commits += len(get_commits_for_repo(username, repo["name"]))

    print(f"Username: {username}")
    print(f"Public repos: {total_repos}")
    print(f"Total stars: {total_stars}")
    print(f"Total commits: {total_commits}")
    print(f'Languages: {", ".join(languages)}')


# Use the function
evaluate_applicant("octocat")
