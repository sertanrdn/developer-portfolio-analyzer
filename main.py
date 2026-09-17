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
    print(url)

    response = requests.get(url)
    print(response.status_code)

    repositories = response.json()
    print(type(repositories))