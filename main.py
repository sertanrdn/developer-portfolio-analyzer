import os
import sys

from dotenv import load_dotenv
import requests
from analysis import (
    process_repositories,
    get_repository_summary,
    analyze_languages,
    analyze_detailed_languages,
    analyze_metadata_coverage,
    analyze_recent_activity,
    analyze_readme_coverage
) 

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    print("Error: GitHub token not found.")
    sys.exit(1)
print("GitHub token loaded successfully.")

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

    page = 1
    repositories = []
    fetch_successful = False

    while True:
        parameters = {
            "per_page": 100,
            "page": page
        }

        try:
            response = requests.get(
                url, headers=request_headers, params=parameters, timeout=10
            )
        except requests.exceptions.Timeout:
            print("Error: GitHub request timed out.")
            break
        except requests.exceptions.ConnectionError:
            print("Error: could not connect to GitHub.")
            break
        except requests.exceptions.RequestException:
            print("Error: GitHub request failed.")
            break

        if response.status_code == 200:
            page_repositories = response.json()

            if not page_repositories:
                fetch_successful = True
                break
        
            repositories.extend(page_repositories)
            page += 1
        elif response.status_code == 404:
            print("Error: GitHub user not found.")
            break
        else:
            print(f"Error: GitHub request failed with status code {response.status_code}.")
            break
    
    if fetch_successful:
        processed_repositories = process_repositories(repositories)

        readme_results = []
        for repository in processed_repositories:
            if not repository.get("fork"):
                repo_name = repository.get("name")
                readme_url = f"https://api.github.com/repos/{cleaned_username}/{repo_name}/readme"

                readme_response = requests.get(
                    readme_url, headers=request_headers, timeout=10
                )

                if readme_response.status_code == 200:
                    readme_data = {
                        "repo_name": repo_name,
                        "has_readme": True
                    }
                    readme_results.append(readme_data)
                elif readme_response.status_code == 404:
                    readme_data = {
                        "repo_name": repo_name,
                        "has_readme": False
                    }
                    readme_results.append(readme_data)
                else:
                    readme_data = {
                        "repo_name": repo_name,
                        "has_readme": None
                    }
                    readme_results.append(readme_data)

        language_results = []
        for repository in processed_repositories:
            if not repository.get("fork"):
                repo_name = repository.get("name")
                language_url = f"https://api.github.com/repos/{cleaned_username}/{repo_name}/languages"

                language_response = requests.get(
                    language_url, headers=request_headers, timeout=10
                )

                if language_response.status_code == 200:
                    language_dict = language_response.json()
                    language_data = {
                        "repo_name": repo_name,
                        "languages": language_dict
                    }
                    language_results.append(language_data)

        repository_summary = get_repository_summary(processed_repositories)
        language_counts, no_language_count = analyze_languages(processed_repositories)
        language_repo_counts, no_language_data_count = analyze_detailed_languages(language_results)

        original_repositories = repository_summary["original"]
        metadata_analysis = analyze_metadata_coverage(
            processed_repositories,
            original_repositories
        )
        sorted_repositories, recently_active_count = analyze_recent_activity(
            processed_repositories
        )

        readme_analysis = analyze_readme_coverage(readme_results)

        print("Total repositories:", repository_summary["total"])
        print("Original repositories:", repository_summary["original"])
        print("Forked repositories:", repository_summary["forked"])
        print("Archived original repositories:", repository_summary["archived"])

        print("Primary languages (original repositories):")
        for language, count in language_counts.items():
            print(language, count, sep=": ")
        print("No primary language:", no_language_count)

        print("Languages across original repositories:")
        for language, count in language_repo_counts.items():
            print(language, count, sep=": ")
        print("No detected language data:", no_language_data_count)

        print("Description coverage:")
        print("With description:", metadata_analysis["with_description"])
        print("Without description:", metadata_analysis["without_description"])
        print(f"Coverage: {metadata_analysis['description_coverage']}%")

        print("Topics coverage:")
        print("With topics:", metadata_analysis["with_topics"])
        print("Without topics:", metadata_analysis["without_topics"])
        print(f"Coverage: {metadata_analysis['topics_coverage']}%")

        print(f"Recently active original repositories (last 90 days): {recently_active_count} of {original_repositories}")
        print("Recently updated repositories:")
        for repository in sorted_repositories[:3]:
            repo_name = repository.get("name")
            pushed_at = repository.get("pushed_at")

            formatted_date = pushed_at.strftime("%Y-%m-%d")

            print(f"{repo_name} — {formatted_date}")

        print("README coverage:")
        print("With README:", readme_analysis["with_readme"])
        print("Without README:", readme_analysis["without_readme"])
        print("Unknown README status:", readme_analysis["unknown_readme"])
        print(f"Coverage: {readme_analysis['readme_coverage']}%")