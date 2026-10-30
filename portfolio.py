from analysis import (
    process_user_profile,
    process_repositories,
    get_repository_summary,
    analyze_languages,
    analyze_detailed_languages,
    analyze_metadata_coverage,
    analyze_recent_activity,
    analyze_readme_coverage,
    build_repository_details
)

from github_api import (
    fetch_user_profile,
    fetch_repositories,
    fetch_readme_data,
    fetch_language_data
)


def analyze_portfolio(username, github_token):
    # Fetch and process GitHub profile
    user_profile = fetch_user_profile(
        username=username,
        github_token=github_token
    )
    processed_user_profile = process_user_profile(user_profile)

    # Fetch and process repositories
    repositories = fetch_repositories(
        username=username,
        github_token=github_token
    )
    processed_repositories = process_repositories(repositories)

    # Fetch additional repository data
    readme_results = fetch_readme_data(
        username=username,
        repositories=processed_repositories,
        github_token=github_token
    )

    language_results = fetch_language_data(
        username=username,
        repositories=processed_repositories,
        github_token=github_token
    )

    # Run analysis
    repository_summary = get_repository_summary(processed_repositories)

    (
        language_counts,
        no_language_count,
        primary_language_percentages
    ) = analyze_languages(processed_repositories)

    (
        language_repo_counts,
        no_language_data_count,
        unknown_language_count
    ) = analyze_detailed_languages(language_results)

    metadata_analysis = analyze_metadata_coverage(
        processed_repositories,
        repository_summary["original"]
    )

    readme_analysis = analyze_readme_coverage(readme_results)

    (
        sorted_repositories,
        recently_active_count,
        freshness_buckets
    ) = analyze_recent_activity(processed_repositories)

    repository_details = build_repository_details(
        processed_repositories,
        readme_results,
        language_results
    )

    # Return all results in one dictionary
    return {
        "profile": processed_user_profile,
        "repositories": processed_repositories,
        "repository_summary": repository_summary,
        "language_counts": language_counts,
        "no_language_count": no_language_count,
        "primary_language_percentages": primary_language_percentages,
        "detailed_language_counts": language_repo_counts,
        "no_language_data_count": no_language_data_count,
        "unknown_language_count": unknown_language_count,
        "metadata_analysis": metadata_analysis,
        "readme_results": readme_results,
        "readme_analysis": readme_analysis,
        "language_results": language_results,
        "freshness_buckets": freshness_buckets,
        "sorted_repositories": sorted_repositories,
        "recently_active_count": recently_active_count,
        "repository_details": repository_details
    }