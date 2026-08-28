import os
from dulwich import porcelain

def main():
    repo_path = os.getcwd()
    print("Initializing repository at:", repo_path)
    
    # Initialize repo if not already
    try:
        repo = porcelain.open_repo(repo_path)
        print("Existing repo found.")
    except Exception:
        repo = porcelain.init(repo_path)
        print("Initialized new Git repo.")

    # Add files
    print("Staging files...")
    porcelain.add(repo_path)

    # Commit
    try:
        commit_id = porcelain.commit(
            repo_path,
            message="Initial commit: AI-Powered Quiz Generator with Groq and ChromaDB".encode('utf-8'),
            author="VinayGT <vinay@example.com>".encode('utf-8')
        )
        print("Committed successfully with ID:", commit_id.decode('utf-8') if isinstance(commit_id, bytes) else commit_id)
    except Exception as e:
        print("Commit status/notice:", str(e))

if __name__ == "__main__":
    main()
