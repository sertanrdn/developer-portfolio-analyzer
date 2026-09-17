import requests

username = input("Enter GitHub username: ")
cleaned_username = username.strip()

if not cleaned_username:
    print("Error: GitHub username is required.")
else:
    print("GitHub username:", cleaned_username)

    url = f"https://api.github.com/users/{cleaned_username}/repos"
    print(url)

    response = requests.get(url)
    print(response.status_code)

    repositories = response.json()
    print(type(repositories))