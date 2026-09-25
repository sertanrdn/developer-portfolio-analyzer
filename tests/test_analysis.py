from analysis import (
    process_repositories,
    get_repository_summary,
    analyze_languages, 
    analyze_detailed_languages,
    analyze_recent_activity,
    analyze_readme_coverage,
    analyze_metadata_coverage
)

def test_process_repositories():
    repositories = [
        {
            "id": 12345,
            "name": "project-a",
            "description": "My Python project",
            "language": "Python",
            "topics": ["python", "api"],
            "fork": False,
            "archived": False,
            "created_at": "2026-01-01T10:00:00Z",
            "pushed_at": "2026-09-20T10:00:00Z"
        }
    ]

    result = process_repositories(repositories=repositories)

    assert result == [
        {
            "name": "project-a",
            "description": "My Python project",
            "language": "Python",
            "topics": ["python", "api"],
            "fork": False,
            "archived": False,
            "created_at": "2026-01-01T10:00:00Z",
            "pushed_at": "2026-09-20T10:00:00Z"
        }
    ]

def test_repository_summary_counts():
    repositories = [
        {
            "fork": False, 
            "archived": False
        },
        {
            "fork": False, 
            "archived": True
        },
        {
            "fork": True, 
            "archived": False
        }
    ]

    repo_summary = get_repository_summary(processed_repositories=repositories)

    assert repo_summary["total"] == 3
    assert repo_summary["original"] == 2
    assert repo_summary["forked"] == 1
    assert repo_summary["archived"] == 1

def test_analyze_languages():
    repositories = [
        {"fork": False, "language": "Python"},
        {"fork": False, "language": "Python"},
        {"fork": False, "language": "JavaScript"},
        {"fork": False, "language": None},
        {"fork": True, "language": "Python"}
    ]

    language_counts, no_language_count = analyze_languages(processed_repositories=repositories)

    assert language_counts == {
        "Python": 2,
        "JavaScript": 1
    }
    assert no_language_count == 1

def test_analyze_detailed_languages():
    language_results = [
        {
            "repo_name": "project-a",
            "languages": {"Python": 1000, "HTML": 200}
        },
        {
            "repo_name": "project-b",
            "languages": {"Python": 500, "JavaScript": 300}
        },
        {
            "repo_name": "project-c",
            "languages": {}
        },
        {
            "repo_name": "project-d",
            "languages": None
        }
    ]

    language_repo_counts, no_language_data_count, unknown_language_count = (
        analyze_detailed_languages(language_results)
    )

    assert language_repo_counts == {
        "Python": 2,
        "HTML": 1,
        "JavaScript": 1
    }
    assert no_language_data_count == 1
    assert unknown_language_count == 1

def test_metadata_coverage():
    repositories = [
        {
            "fork": False,
            "description": "Project A description",
            "topics": ["python"]
        },
        {
            "fork": False,
            "description": "Project B description",
            "topics": []
        },
        {
            "fork": False,
            "description": None,
            "topics": []
        },
        {
            "fork": True,
            "description": "Fork description",
            "topics": ["javascript"]
        }
    ]
    original_repositories = 3

    metadata_result = analyze_metadata_coverage(
        processed_repositories=repositories, 
        original_repositories=original_repositories
    )

    assert metadata_result["with_description"] == 2
    assert metadata_result["without_description"] == 1
    assert metadata_result["description_coverage"] == 66.67
    assert metadata_result["with_topics"] == 1
    assert metadata_result["without_topics"] == 2
    assert metadata_result["topics_coverage"] == 33.33

def test_analyze_recent_activity():
    repositories = [
        {
            "name": "recent-project",
            "fork": False,
            "pushed_at": "2026-09-20T10:00:00+00:00"
        },
        {
            "name": "older-project",
            "fork": False,
            "pushed_at": "2025-01-01T10:00:00+00:00"
        },
        {
            "name": "forked-project",
            "fork": True,
            "pushed_at": "2026-09-24T10:00:00+00:00"
        }
    ]

    sorted_repositories, _ = analyze_recent_activity(repositories)

    assert len(sorted_repositories) == 2
    assert sorted_repositories[0]["name"] == "recent-project"
    assert sorted_repositories[1]["name"] == "older-project"

def test_analyze_readme_coverage():
    readme_results = [
        {"repo_name": "project-a", "has_readme": True},
        {"repo_name": "project-b", "has_readme": True},
        {"repo_name": "project-c", "has_readme": False},
        {"repo_name": "project-d", "has_readme": None}
    ]

    result = analyze_readme_coverage(readme_results)

    assert result == {
        "with_readme": 2,
        "without_readme": 1,
        "unknown_readme": 1,
        "readme_coverage": 66.67
    }