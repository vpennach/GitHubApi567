import requests
import json

def get_repos_and_commits(username):
    
        #Strips the username so if it is input with spaces it still works
    username = username.strip()
    
    account_url = f"https://api.github.com/users/{username}/repos"
        
    try:
        #Get a list of the repositories
        repos_response = requests.get(account_url)
        
        #Error handling (checking for correct response)
        
        if repos_response.status_code == 404:
            return f"Error: Username '{username} not found"
        if repos_response.status_code != 200:
            return f"Error: Unable to fetch data"
        
        repos = repos_response.json()
        repos_commits_list = []
        
        #For each repository fetch the number of commits
        for repo in repos:
            repo_name = repo['name']
            commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
            
            commits_response = requests.get(commits_url)
            
            if commits_response.status_code != 200:
                print("Error fetching commits")
                continue
            
            commits = commits_response.json()
            repo_info = f"Repo: {repo_name} Number of commits: {len(commits)}"
            repos_commits_list.append(repo_info)
        
        return repos_commits_list
    except requests.exceptions.RequestException as e:
        return f"Error: A network error occured"
    
username = "  Vpennach"
repos_commits = get_repos_and_commits(username)

print(repos_commits)