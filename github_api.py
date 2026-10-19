import requests

class GitHubError(Exception):
    pass

class GitHubUserNotFoundError(GitHubError):
    pass

class GitHubAuthenticationError(GitHubError):
    pass

class GitHubRateLimitError(GitHubError):
    pass

class GitHubRequestError(GitHubError):
    pass

def create_headers(token):
    request_headers = {
        "Authorization": f"Bearer {token}"
    }
    return request_headers

def fetch_user_profile(username, github_token):
    # Get the profile data from github api
    url = f"https://api.github.com/users/{username}"

    request_headers = create_headers(token=github_token)

    try:
        response = requests.get(url, headers=request_headers, timeout=10)
    except requests.exceptions.Timeout:
        raise GitHubRequestError("GitHub request timed out.")
    except requests.exceptions.ConnectionError:
        raise GitHubRequestError("Could not connect to GitHub.")
    except requests.exceptions.RequestException:
        raise GitHubRequestError("GitHub request failed due to a network or request error.")

    if response.status_code == 200:
        return response.json()
    
    elif response.status_code == 404:
        raise GitHubUserNotFoundError("GitHub user not found.")
    elif response.status_code == 401:
        raise GitHubAuthenticationError("Authentication failed. Please check your GitHub token or credentials.")
    elif response.status_code == 403:
        remaining_requests = response.headers.get("X-RateLimit-Remaining")

        if remaining_requests == "0":
            raise GitHubRateLimitError("You have hit your GitHub API request limit.")
        else:
            raise GitHubRequestError("GitHub denied the request.")

    else:
        raise GitHubRequestError(f"GitHub request failed with status code {response.status_code}.")

def fetch_repositories(username, github_token):
    # Get the repo data from github api
    url = f"https://api.github.com/users/{username}/repos"

    request_headers = create_headers(token=github_token)

    page = 1
    repositories = []

    while True:
        parameters = {
            "per_page": 100,
            "page": page
        }

        try:
            response = requests.get(
                url, headers=request_headers, params=parameters, timeout=10
            )
        except requests.exceptions.Timeout:
            raise GitHubRequestError("GitHub request timed out.")
        except requests.exceptions.ConnectionError:
            raise GitHubRequestError("Could not connect to GitHub.")
        except requests.exceptions.RequestException:
            raise GitHubRequestError("GitHub request failed due to a network or request error.")

        if response.status_code == 200:
            page_repositories = response.json()

            if not page_repositories:
                return repositories
        
            repositories.extend(page_repositories)
            page += 1
        elif response.status_code == 404:
            raise GitHubUserNotFoundError("GitHub user not found.")
        elif response.status_code == 401:
            raise GitHubAuthenticationError("Authentication failed. Please check your GitHub token or credentials.")
        elif response.status_code == 403:
            remaining_requests = response.headers.get("X-RateLimit-Remaining")

            if remaining_requests == "0":
                raise GitHubRateLimitError("You have hit your GitHub API request limit.")
            else:
                raise GitHubRequestError("GitHub denied the request.")

        else:
            raise GitHubRequestError(f"GitHub request failed with status code {response.status_code}.")

def make_readme_entry(repo_name, has_readme, error=None):
    return {"repo_name": repo_name, "has_readme": has_readme, "error": error}
  
def fetch_readme_data(username, repositories, github_token):
    readme_results = []
    request_headers = create_headers(token=github_token)
    stop_reason = None

    for repository in repositories:
        if repository.get("fork"):
            continue

        repo_name = repository.get("name")

        if stop_reason:
            readme_results.append(
                make_readme_entry(repo_name, None, f"skipped: {stop_reason}")
            )
            continue

        readme_url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
            
        try:
            readme_response = requests.get(
                readme_url, headers=request_headers, timeout=10
            )

        except requests.exceptions.Timeout:    
            readme_results.append(make_readme_entry(repo_name, None, "timed out"))
            continue
        except requests.exceptions.ConnectionError:
            readme_results.append(make_readme_entry(repo_name, None, "could not connect"))
            continue
        except requests.exceptions.RequestException:
            readme_results.append(make_readme_entry(repo_name, None, "request failed"))
            continue

        if readme_response.status_code == 200:
            readme_results.append(make_readme_entry(repo_name, True))

        elif readme_response.status_code == 404:
            readme_results.append(make_readme_entry(repo_name, False))
        elif readme_response.status_code == 401:
            stop_reason = "authentication failed"
            readme_results.append(
                make_readme_entry(repo_name, None, stop_reason)
            )
        elif readme_response.status_code == 403:
            if readme_response.headers.get("X-RateLimit-Remaining") == "0":
                stop_reason = "rate limit reached"
            else:
                readme_results.append(
                    make_readme_entry(repo_name, None, "access denied")
                )
                continue

            readme_results.append(
                make_readme_entry(repo_name, None, stop_reason)
            )
        else:
            readme_results.append(
                make_readme_entry(
                    repo_name, None, f"status {readme_response.status_code}"
                )
            )

    return readme_results

def fetch_language_data(username, repositories, github_token):
    language_results = []
    request_headers = create_headers(token=github_token)
    
    for repository in repositories:
        if not repository.get("fork"):
            repo_name = repository.get("name")
            language_url = f"https://api.github.com/repos/{username}/{repo_name}/languages"

            try:
                language_response = requests.get(
                    language_url, headers=request_headers, timeout=10
                )
            except requests.exceptions.Timeout:
                print(f"Warning: Language request timed out for {repo_name}.")
                language_data = {
                    "repo_name": repo_name,
                    "languages": None
                }
                language_results.append(language_data)
                continue

            except requests.exceptions.ConnectionError:
                print(f"Warning: Could not connect to GitHub while checking languages for {repo_name}.")
                language_data = {
                    "repo_name": repo_name,
                    "languages": None
                }
                language_results.append(language_data)
                continue

            except requests.exceptions.RequestException:
                print(f"Warning: Language request failed for {repo_name}.")
                language_data = {
                    "repo_name": repo_name,
                    "languages": None
                }
                language_results.append(language_data)
                continue

            if language_response.status_code == 200:
                language_dict = language_response.json()
                language_data = {
                    "repo_name": repo_name,
                    "languages": language_dict
                }
                language_results.append(language_data)
            elif language_response.status_code == 401:
                print(f"Warning: Authentication failed while checking languages for {repo_name}.")
                language_data = {
                    "repo_name": repo_name,
                    "languages": None
                }
                language_results.append(language_data)
            elif language_response.status_code == 403:
                print(f"Warning: GitHub denied the languages request for {repo_name}.")
                language_data = {
                    "repo_name": repo_name,
                    "languages": None
                }
                language_results.append(language_data)
            else:
                language_data = {
                    "repo_name": repo_name,
                    "languages": None
                }
                language_results.append(language_data)

    return language_results