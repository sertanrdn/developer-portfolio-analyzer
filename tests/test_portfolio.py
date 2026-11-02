from unittest.mock import patch

import pytest

from github_api import GitHubUserNotFoundError
from portfolio import analyze_portfolio


def make_raw_repository(name, fork=False):
    return {
        "name": name,
        "description": "A project",
        "html_url": f"https://github.com/testuser/{name}",
        "language": "Python",
        "topics": [],
        "fork": fork,
        "archived": False,
        "stargazers_count": 0,
        "forks_count": 0,
        "created_at": "2026-01-01T10:00:00+00:00",
        "pushed_at": "2026-09-20T10:00:00+00:00",
    }


def test_analyze_portfolio_keeps_unknown_results_unknown():
    readme_results = [
        {"repo_name": "project-a", "has_readme": True, "error": None},
        {"repo_name": "project-b", "has_readme": None, "error": "timed out"},
    ]
    language_results = [
        {"repo_name": "project-a", "languages": {"Python": 1000}, "error": None},
        {"repo_name": "project-b", "languages": None, "error": "timed out"},
    ]

    with (
        patch("portfolio.fetch_user_profile") as mock_profile,
        patch("portfolio.fetch_repositories") as mock_repositories,
        patch("portfolio.fetch_readme_data") as mock_readme,
        patch("portfolio.fetch_language_data") as mock_language,
    ):
        mock_profile.return_value = {"login": "testuser"}
        mock_repositories.return_value = [
            make_raw_repository("project-a"),
            make_raw_repository("project-b"),
            make_raw_repository("project-c", fork=True),
        ]
        mock_readme.return_value = readme_results
        mock_language.return_value = language_results

        result = analyze_portfolio(username="testuser", github_token="test-token")

    assert result["repository_summary"]["original"] == 2
    assert result["repository_summary"]["forked"] == 1
    assert result["readme_analysis"]["unknown_readme"] == 1
    assert result["readme_analysis"]["without_readme"] == 0
    assert result["unknown_language_count"] == 1
    assert result["readme_results"] is readme_results


def test_analyze_portfolio_propagates_errors_and_stops():
    with (
        patch("portfolio.fetch_user_profile") as mock_profile,
        patch("portfolio.fetch_repositories") as mock_repositories,
    ):
        mock_profile.side_effect = GitHubUserNotFoundError("GitHub user not found.")

        with pytest.raises(GitHubUserNotFoundError):
            analyze_portfolio(username="testuser", github_token="test-token")

        mock_repositories.assert_not_called()