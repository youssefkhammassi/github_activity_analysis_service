def generate_github_events_url(repo: str, owner: str):
    return f'https://api.github.com/repos/{owner}/{repo}/events'
