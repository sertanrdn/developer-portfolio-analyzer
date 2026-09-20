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

    # Get the repo data from github api
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

    # Get the repo summary count
    total_repositories = len(processed_repositories)
    forked_repositories = 0
    archived_repositories = 0

    for repository in processed_repositories:
        if repository.get("fork"):
            forked_repositories += 1
        
        if repository.get("archived"):
            archived_repositories += 1
    
    original_repositories = total_repositories - forked_repositories

    print("Total repositories:", total_repositories)
    print("Original repositories:", original_repositories)
    print("Forked repositories:", forked_repositories)
    print("Archived repositories:", archived_repositories)

    # Language analysis for repos
    language_counts = {}
    no_language_count = 0

    for repository in processed_repositories:
        if not repository.get("fork"):
            language = repository.get("language")

            if language is None:
                no_language_count += 1
            else:
                if language in language_counts:
                    language_counts[language] += 1
                else:
                    language_counts[language] = 1

    print("Primary languages (original repositories):")
    for language, count in language_counts.items():
        print(language, count, sep=": ")
    print("No primary language:", no_language_count)

    # Get the description and topic coverages for repos
    repo_with_desc = 0
    repo_without_desc = 0

    for repository in processed_repositories:
        if not repository.get("fork"):
            if repository.get("description"):
                repo_with_desc += 1
            else:
                repo_without_desc += 1

    repo_with_topics = 0
    repo_without_topics = 0

    for repository in processed_repositories:
        if not repository.get("fork"):
            if repository.get("topics"):
                repo_with_topics += 1
            else: 
                repo_without_topics += 1

    description_coverage = round((repo_with_desc / original_repositories) * 100, 2)
    topics_coverage = round((repo_with_topics / original_repositories) * 100, 2)

    print("Description coverage:")
    print("With description:", repo_with_desc)
    print("Without description:", repo_without_desc)
    print(f"Coverage: {description_coverage}%")

    print("Topics coverage:")
    print("With topics:", repo_with_topics)
    print("Without topics:", repo_without_topics)
    print(f"Coverage: {topics_coverage}%")