def generate_github_events_url(repo: str, owner: str):
    """
    generate GitHub events url
    input:
        repo: str
        owner: str
    output: str
    """
    return f'https://api.github.com/repos/{owner}/{repo}/events'
