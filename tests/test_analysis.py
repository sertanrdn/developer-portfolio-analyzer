from analysis import (
    process_repositories,
    get_repository_summary,
    analyze_languages, 
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