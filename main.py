import os

from dotenv import load_dotenv
import requests
from datetime import datetime, timezone

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

if github_token:
    print("Github token loaded successfully")
else:
    print("Error: GitHub token not found.")

username = input("Enter GitHub username: ")
cleaned_username = username.strip()

def process_repositories(repositories):
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
    return processed_repositories

def get_repository_summary(processed_repositories):
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

    summary_repositories = {
        "total": total_repositories,
        "original": original_repositories,
        "forked": forked_repositories,
        "archived": archived_repositories
    }

    return summary_repositories

def analyze_languages(processed_repositories):
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

    return language_counts, no_language_count

def analyze_metadata_coverage(processed_repositories, original_repositories):
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

    if original_repositories > 0:
        description_coverage = round((repo_with_desc / original_repositories) * 100, 2)
        topics_coverage = round((repo_with_topics / original_repositories) * 100, 2)
    else:
        description_coverage = 0
        topics_coverage = 0

    metadata_analysis = {
        "with_description": repo_with_desc,
        "without_description": repo_without_desc,
        "description_coverage": description_coverage,
        "with_topics": repo_with_topics,
        "without_topics": repo_without_topics,
        "topics_coverage": topics_coverage
    }

    return metadata_analysis

def analyze_recent_activity(processed_repositories):
    # Calculating the recent activity
    recent_repositories = []

    for repository in processed_repositories:
        if not repository.get("fork"):
            date_string = repository.get("pushed_at")

            if date_string:
                date_object = datetime.fromisoformat(date_string)

                activity_data = {
                    "name": repository.get("name"),
                    "pushed_at": date_object
                }
                recent_repositories.append(activity_data)

    sorted_repositories = sorted(
        recent_repositories,
        key=lambda repository: repository["pushed_at"],
        reverse=True
    )

    # Get the activity within last 90 days
    recently_active_count = 0
    current_time = datetime.now(timezone.utc)

    for repository in sorted_repositories:
        time_since_push = current_time - repository["pushed_at"]

        if time_since_push.days <= 90:
            recently_active_count += 1

    return sorted_repositories, recently_active_count

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

    if response.status_code == 200:
        repositories = response.json()

        processed_repositories = process_repositories(repositories)
        repository_summary = get_repository_summary(processed_repositories)
        language_counts, no_language_count = analyze_languages(processed_repositories)

        original_repositories = repository_summary["original"]
        metadata_analysis = analyze_metadata_coverage(
            processed_repositories,
            original_repositories
        )
        sorted_repositories, recently_active_count = analyze_recent_activity(
            processed_repositories
        )

        print("Total repositories:", repository_summary["total"])
        print("Original repositories:", repository_summary["original"])
        print("Forked repositories:", repository_summary["forked"])
        print("Archived repositories:", repository_summary["archived"])

        print("Primary languages (original repositories):")
        for language, count in language_counts.items():
            print(language, count, sep=": ")
        print("No primary language:", no_language_count)

        print("Description coverage:")
        print("With description:", metadata_analysis["with_description"])
        print("Without description:", metadata_analysis["without_description"])
        print(f"Coverage: {metadata_analysis['description_coverage']}%")

        print("Topics coverage:")
        print("With topics:", metadata_analysis["with_topics"])
        print("Without topics:", metadata_analysis["without_topics"])
        print(f"Coverage: {metadata_analysis['topics_coverage']}%")

        print(f"Recently active original repositories (last 90 days): {recently_active_count} of {original_repositories}")
    elif response.status_code == 404:
        print("Error: GitHub user not found.")
    else:
        print(f"Error: GitHub request failed with status code {response.status_code}.")