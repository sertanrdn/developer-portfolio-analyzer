import os
import sys

from dotenv import load_dotenv
from github_api import GitHubError
from portfolio import analyze_portfolio

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
    sys.exit(1)
else:
    print("GitHub username:", cleaned_username)

    try:
        analysis_result = analyze_portfolio(
            username=cleaned_username,
            github_token=github_token
        )

    except GitHubError as error:
        print(f"Error analyzing GitHub portfolio: {error}")
        sys.exit(1)

    # Extract results for terminal presentation
    processed_user_profile = analysis_result["profile"]
    repository_summary = analysis_result["repository_summary"]
    original_repositories = repository_summary["original"]

    language_counts = analysis_result["language_counts"]
    no_language_count = analysis_result["no_language_count"]
    primary_language_percentages = analysis_result["primary_language_percentages"]

    language_repo_counts = analysis_result["detailed_language_counts"]
    no_language_data_count = analysis_result["no_language_data_count"]
    unknown_language_count = analysis_result["unknown_language_count"]

    metadata_analysis = analysis_result["metadata_analysis"]
    readme_analysis = analysis_result["readme_analysis"]

    sorted_repositories = analysis_result["sorted_repositories"]
    recently_active_count = analysis_result["recently_active_count"]
    freshness_buckets = analysis_result["freshness_buckets"]

    readme_results = analysis_result["readme_results"]
    language_results = analysis_result["language_results"]


    # Print individual warnings
    for result in readme_results:
        if result.get("error"):
            print(
                f"Warning: README check for "
                f"{result['repo_name']}: {result['error']}"
            )

    for result in language_results:
        if result.get("error"):
            print(
                f"Warning: language check for "
                f"{result['repo_name']}: {result['error']}"
            )

    print("")
    print("GitHub Profile")
    print("--------------")
    print("Username:", processed_user_profile.get("login"))
    print("Name:", processed_user_profile.get("name") or "Not provided")
    print("Bio:", processed_user_profile.get("bio") or "Not provided")
    print("Location:", processed_user_profile.get("location") or "Not provided")
    print("Company:", processed_user_profile.get("company") or "Not provided")
    print("Blog:", processed_user_profile.get("blog") or "Not provided")
    print("Public repositories:", processed_user_profile.get("public_repos"))
    print("Followers:", processed_user_profile.get("followers"))
    print("Following:", processed_user_profile.get("following"))
    print("GitHub profile:", processed_user_profile.get("html_url"))
    print("Member since:", processed_user_profile.get("created_at"))

    print("")
    print("Repository Analysis")
    print("-------------------")

    print("Total repositories:", repository_summary["total"])
    print("Original repositories:", repository_summary["original"])
    print("Forked repositories:", repository_summary["forked"])
    print("Archived original repositories:", repository_summary["archived"])

    print("Primary languages (original repositories):")
    for language, count in language_counts.items():
        print(language, count, sep=": ")
    print("No primary language:", no_language_count)

    print("Primary language distribution:")
    for language, percentage in primary_language_percentages.items():
        print(f"{language}: {percentage}%")

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
    print("Repository freshness:")
    print("Last 90 days:", freshness_buckets["last_90_days"])
    print("91–365 days:", freshness_buckets["91_to_365_days"])
    print("1–2 years:", freshness_buckets["1_to_2_years"])
    print("Over 2 years:", freshness_buckets["over_2_years"])

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