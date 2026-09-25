import requests

from unittest.mock import Mock, patch

from github_api import fetch_repositories

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