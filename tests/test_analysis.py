from analysis import get_repository_summary, analyze_metadata_coverage

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