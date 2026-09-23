from datetime import datetime, timezone

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
        
        if repository.get("archived") and not repository.get("fork"):
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

def analyze_detailed_languages(language_results):
    language_repo_counts = {}
    no_language_data_count = 0
    unknown_language_count = 0

    for repository in language_results:
        languages_dict = repository.get("languages")

        if languages_dict is None:
            unknown_language_count += 1
        elif not languages_dict:
            no_language_data_count += 1
        else:
            for language in languages_dict:
                if language in language_repo_counts:
                    language_repo_counts[language] += 1
                else:
                    language_repo_counts[language] = 1
    
    return language_repo_counts, no_language_data_count, unknown_language_count

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
    # Calculate recent activity
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

def analyze_readme_coverage(readme_results):
    with_readme = 0
    without_readme = 0
    unknown_readme = 0

    for repository in readme_results:
        has_readme = repository.get("has_readme")
        if has_readme is True:
            with_readme += 1
        elif has_readme is False:
            without_readme += 1
        else:
            unknown_readme += 1

    known_readme_results = with_readme + without_readme

    if known_readme_results > 0:
        readme_coverage = round((with_readme / known_readme_results) * 100, 2)
    else:
        readme_coverage = 0
    
    readme_data = {
        "with_readme": with_readme,
        "without_readme": without_readme,
        "unknown_readme": unknown_readme,
        "readme_coverage": readme_coverage
    }

    return readme_data