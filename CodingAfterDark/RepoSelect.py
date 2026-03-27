"""
Search github for top repos accross top languages
"""

from github import Github
from dotenv import load_dotenv
import os, time

load_dotenv()
g = Github(os.getenv("GITHUB_TOKEN"))

# top lanuages to sample
LANGUAGES = ["python", "java", "javascript", "C", "C++"]
REPOS_PER_LANGUAGE=100

output_file = "repos.txt"
collected = []

def is_qualified(repo):
    # not a fork
    if repo.fork:
        return False
    
    # blacklist
    name = (repo.name).lower()
    blacklist = ["awesome", "tutorial", "learning", "beginner"
                 "course", "guide", "cheatsheet", "interview"]

    for word in blacklist:
        if word in name:
            return False, "got blacklisted keyword"
    
    return True, "passed"

for lang in LANGUAGES:
    
    # criteria
    query = f"stars:>3000 forks:>500 languages{lang} pushed:> 2024-01-01"
    results = g.search_repositories(query=query, sort="updated", order="desc")

    for repo in results:
        qualified, reason = is_qualified(repo)
        if not qualified:
            print(f"Not taking {repo.full_name} - {reason}")
            continue

        collected.append(repo.fullname)
        time.sleep(0.5) # mercy to the API call

# save to file
with open(output_file, "w") as f:
    for repo in collected:
        f.write(repo + "\n")

print(f"total {len(collected)} repos saved")