import os
import sys

from dotenv import load_dotenv
from analysis import (
    process_repositories,
    get_repository_summary,
    analyze_languages,
    analyze_detailed_languages,
    analyze_metadata_coverage,
    analyze_recent_activity,
    analyze_readme_coverage
) 
from github_api import (
    fetch_repositories,
    fetch_readme_data,
    fetch_language_data
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

    repositories = fetch_repositories(
        username=cleaned_username, github_token=github_token
    )
    
    if repositories is not None:
        processed_repositories = process_repositories(repositories)
        readme_results = fetch_readme_data(
            username=cleaned_username, repositories=processed_repositories, github_token=github_token
        )
        language_results = fetch_language_data(
            username=cleaned_username, repositories=processed_repositories, github_token=github_token
        )

        repository_summary = get_repository_summary(processed_repositories)
        language_counts, no_language_count = analyze_languages(processed_repositories)
        language_repo_counts, no_language_data_count, unknown_language_count = analyze_detailed_languages(language_results)

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
        print("Unknown language status:", unknown_language_count)

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