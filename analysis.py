from datetime import datetime, timezone

def process_user_profile(user_profile):
    profile_data = {
        "login": user_profile.get("login"),
        "name": user_profile.get("name"),
        "avatar_url": user_profile.get("avatar_url"),
        "html_url": user_profile.get("html_url"),
        "bio": user_profile.get("bio"),
        "company": user_profile.get("company"),
        "blog": user_profile.get("blog"),
        "location": user_profile.get("location"),
        "public_repos": user_profile.get("public_repos"),
        "followers": user_profile.get("followers"),
        "following": user_profile.get("following"),
        "created_at": user_profile.get("created_at")
    }

    return profile_data

def process_repositories(repositories):
    processed_repositories = []

    for repository in repositories:
        repo_data = {
            "name": repository.get("name"),
            "description": repository.get("description"),
            "html_url": repository.get("html_url"),
            "language": repository.get("language"),
            "topics": repository.get("topics", []),
            "fork": repository.get("fork"),
            "archived": repository.get("archived"),
            "stargazers_count": repository.get("stargazers_count"),
            "forks_count": repository.get("forks_count"),
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

    repositories_with_language = sum(language_counts.values())
    primary_language_percentages = {}

    if repositories_with_language > 0:
        for language, count in language_counts.items():
            percentage = (count / repositories_with_language) * 100
            primary_language_percentages[language] = round(percentage, 2)

    return language_counts, no_language_count, primary_language_percentages

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

def analyze_recent_activity(processed_repositories, current_time=None):
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

    if current_time is None:
        current_time = datetime.now(timezone.utc)

    freshness_buckets = {
        "last_90_days": 0,
        "91_to_365_days": 0,
        "1_to_2_years": 0,
        "over_2_years": 0
    }

    # Get the activity within last 90 days
    recently_active_count = 0

    for repository in sorted_repositories:
        time_since_push = current_time - repository["pushed_at"]
        days = time_since_push.days

        if days <= 90:
            freshness_buckets["last_90_days"] += 1
            recently_active_count += 1
        elif days <= 365:
            freshness_buckets["91_to_365_days"] += 1
        elif days <= 730:  # 2 years
            freshness_buckets["1_to_2_years"] += 1
        else:
            freshness_buckets["over_2_years"] += 1

    return sorted_repositories, recently_active_count, freshness_buckets

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

def build_repository_details(processed_repositories, readme_results, language_results):
    repository_details = []
    readme_lookup = {}

    for result in readme_results:
        repo_name = result.get("repo_name")
        readme_status = result.get("has_readme")

        readme_lookup[repo_name] = readme_status

    language_lookup = {}
    for result in language_results:
        repo_name = result.get("repo_name")
        language_dict = result.get("languages")

        language_lookup[repo_name] = language_dict

    for repository in processed_repositories:
        if not repository.get("fork"):
            repo_name = repository.get("name")
            readme_status = readme_lookup.get(repo_name)
            languages = language_lookup.get(repo_name)

            if languages is not None:
                language_names = list(languages.keys())
            else:
                language_names = None

            repository_detail = {
                "name": repository.get("name"),
                "description": repository.get("description"),
                "html_url": repository.get("html_url"),
                "primary_language": repository.get("language"),
                "languages": language_names,
                "topics": repository.get("topics"),
                "has_readme": readme_status,
                "stargazers_count": repository.get("stargazers_count"),
                "forks_count": repository.get("forks_count"),
                "pushed_at": repository.get("pushed_at")
            }

            repository_details.append(repository_detail)

    return repository_details