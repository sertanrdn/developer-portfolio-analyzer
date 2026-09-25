import requests

from unittest.mock import Mock, patch

from github_api import (
    fetch_repositories, fetch_readme_data, fetch_language_data
)

# Tests for repository fetching
def test_fetch_repositories_success():
    with patch("github_api.requests.get") as mock_get:
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = [
            {"name": "project-a"},
            {"name": "project-b"}
        ]

        second_response = Mock()
        second_response.status_code = 200
        second_response.json.return_value = []

        mock_get.side_effect = [
            first_response,
            second_response
        ]

        result = fetch_repositories(username="testuser", github_token="test-token")

        assert result == [
            {"name": "project-a"},
            {"name": "project-b"}
        ]
        assert mock_get.call_count == 2

def test_fetch_repositories_user_not_found():
    with patch("github_api.requests.get") as mock_get:
        fake_response = Mock()
        fake_response.status_code = 404
        mock_get.return_value = fake_response

        result = fetch_repositories(username="testuser", github_token="test-token")

        assert result is None
        assert mock_get.call_count == 1
        
def test_fetch_repositories_timeout():
    with patch("github_api.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout

        result = fetch_repositories(username="testuser", github_token="test-token")

        assert result is None
        assert mock_get.call_count == 1

def test_fetch_repositories_rate_limit():
    with patch("github_api.requests.get") as mock_get:
        fake_response = Mock()
        fake_response.status_code = 403
        fake_response.headers = {
            "X-RateLimit-Remaining": "0"
        }
        mock_get.return_value = fake_response

        result = fetch_repositories(username="testuser", github_token="test-token")

        assert result is None
        assert mock_get.call_count == 1

# Tests for readme data fetching
def test_fetch_readme_data():
    repositories = [
        {"name": "project-a", "fork": False},
        {"name": "project-b", "fork": False},
        {"name": "project-c", "fork": True}
    ]

    with patch("github_api.requests.get") as mock_get:
        first_response = Mock()
        first_response.status_code = 200

        second_response = Mock()
        second_response.status_code = 404

        mock_get.side_effect = [first_response, second_response]

        result = fetch_readme_data(
            username="testuser", 
            repositories=repositories, 
            github_token="test-token"
        )

        assert result == [
            {"repo_name": "project-a", "has_readme": True},
            {"repo_name": "project-b", "has_readme": False}
        ]
        assert mock_get.call_count == 2

def test_fetch_readme_data_timeout():
    repositories = [
        {"name": "project-a", "fork": False}
    ]

    with patch("github_api.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout

        result = fetch_readme_data(
            username="testuser", 
            repositories=repositories,
            github_token="test-token"
        )

        assert result == [
            {"repo_name": "project-a", "has_readme": None}
        ]
        assert mock_get.call_count == 1

def test_fetch_language_data():
    repositories = [
        {"name": "project-a", "fork": False},
        {"name": "project-b", "fork": False},
        {"name": "project-c", "fork": True}
    ]

    with patch("github_api.requests.get") as mock_get:
        first_response = Mock()
        first_response.status_code = 200
        first_response.json.return_value = {"Python": 1000, "HTML": 200}

        second_response = Mock()
        second_response.status_code = 200
        second_response.json.return_value = {}

        mock_get.side_effect = [first_response, second_response]

        result = fetch_language_data(
            username="testuser", 
            repositories=repositories, 
            github_token="test-token"
        )

        assert result == [
            {"repo_name": "project-a", "languages": {"Python": 1000, "HTML": 200}},
            {"repo_name": "project-b", "languages": {}}
        ]
        assert mock_get.call_count == 2

def test_fetch_language_data_timeout():
    repositories = [
        {"name": "project-a", "fork": False}
    ]

    with patch("github_api.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout

        result = fetch_language_data(
            username="testuser", 
            repositories=repositories,
            github_token="test-token"
        )

        assert result == [
            {"repo_name": "project-a", "languages": None}
        ]
        assert mock_get.call_count == 1