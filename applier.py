import os

if __name__ == '__main__':
    repo_link = os.environ["REPOSITORY_LINK"]
    run_link = os.environ["ACTION_RUN_LINK"]
    
    print("repo:", repo_link)
    print("run :", run_link)
