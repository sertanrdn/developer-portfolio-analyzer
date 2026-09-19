import os

from dotenv import load_dotenv
import requests

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

if github_token:
    print("Github token loaded successfully")
else:
    print("Error: GitHub token not found.")

username = input("Enter GitHub username: ")
cleaned_username = username.strip()

if not cleaned_username:
    print("Error: GitHub username is required.")
else:
    print("GitHub username:", cleaned_username)

    url = f"https://api.github.com/users/{cleaned_username}/repos"

    request_headers = {
        "Authorization": f"Bearer {github_token}"
    }

    response = requests.get(url, headers=request_headers)
    repositories = response.json()

    processed_repositories = []

    for repository in repositories:
        repo_data = {
            "name": repository.get("name"),
            "description": repository.get("description"),
            "language": repository.get("language"),
            "topics": repository.get("topics", []),
            "fork": repository.get("fork"),
            "archived": repository.get("archived"),
            "created_at": repository.get("created_at"),
            "pushed_at": repository.get("pushed_at")
        }

        processed_repositories.append(repo_data)
    print(processed_repositories)