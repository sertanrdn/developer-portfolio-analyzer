import requests

def fetch_repositories(username, github_token):
    # Get the repo data from github api
    url = f"https://api.github.com/users/{username}/repos"

    request_headers = {
        "Authorization": f"Bearer {github_token}"
    }

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
            print("Error: GitHub request timed out.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to GitHub.")
            return None
        except requests.exceptions.RequestException:
            print("Error: GitHub request failed.")
            return None

        if response.status_code == 200:
            page_repositories = response.json()

            if not page_repositories:
                return repositories
        
            repositories.extend(page_repositories)
            page += 1
        elif response.status_code == 404:
            print("Error: GitHub user not found.")
            return None
        elif response.status_code == 401:
            print("Error: Authentication failed. Please check your GitHub token or credentials.")
            return None
        elif response.status_code == 403:
            remaining_requests = response.headers.get("X-RateLimit-Remaining")

            if remaining_requests == "0":
                print("Rate-limit error: You have hit your GitHub API request limit.")
            else:
                print("Error: GitHub denied the request.")

            return None
        else:
            print(f"Error: GitHub request failed with status code {response.status_code}.")
            return None
        
def fetch_readme_data(username, repositories, github_token):
    readme_results = []
    request_headers = {
        "Authorization": f"Bearer {github_token}"
    }
    for repository in repositories:
        if not repository.get("fork"):
            repo_name = repository.get("name")
            readme_url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
            
            try:
                readme_response = requests.get(
                    readme_url, headers=request_headers, timeout=10
                )

            except requests.exceptions.Timeout:
                print(f"Warning: README request timed out for {repo_name}.")
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": None
                }
                readme_results.append(readme_data)
                continue
            except requests.exceptions.ConnectionError:
                print(f"Warning: Could not connect to GitHub while checking README for {repo_name}.")
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": None
                }
                readme_results.append(readme_data)
                continue
            except requests.exceptions.RequestException:
                print(f"Warning: README request failed for {repo_name}.")
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": None
                }
                readme_results.append(readme_data)
                continue

            if readme_response.status_code == 200:
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": True
                }
                readme_results.append(readme_data)

            elif readme_response.status_code == 404:
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": False
                }
                readme_results.append(readme_data)
            elif readme_response.status_code == 401:
                print(f"Warning: Authentication failed while checking README for {repo_name}.")
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": None
                }
                readme_results.append(readme_data)
            elif readme_response.status_code == 403:
                print(f"Warning: GitHub denied the README request for {repo_name}.")
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": None
                }
                readme_results.append(readme_data)
            else:
                readme_data = {
                    "repo_name": repo_name,
                    "has_readme": None
                }
                readme_results.append(readme_data)

    return readme_results

def fetch_language_data(username, repositories, github_token):
    language_results = []
    request_headers = {
        "Authorization": f"Bearer {github_token}"
    }
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