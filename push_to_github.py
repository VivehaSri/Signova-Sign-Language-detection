"""
Signova AI - GitHub Remote Push Utility
Run this script to push your committed repository to GitHub using your Personal Access Token (PAT).
"""

import sys
import os
import getpass
from dulwich import porcelain

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
REMOTE_REPO = "https://github.com/VivehaSri/Signova-Sign-Language-detection.git"

def push_repo(token=None):
    if not token:
        if len(sys.argv) > 1:
            token = sys.argv[1].strip()
        elif "GITHUB_TOKEN" in os.environ:
            token = os.environ["GITHUB_TOKEN"].strip()
        else:
            print("=" * 60)
            print("🔑 GitHub Personal Access Token (PAT) Required")
            print("To push to https://github.com/VivehaSri/Signova-Sign-Language-detection.git:")
            print("1. Go to https://github.com/settings/tokens")
            print("2. Generate a token with 'repo' scope (or fine-grained write access)")
            print("=" * 60)
            token = getpass.getpass("Enter your GitHub Personal Access Token (input hidden): ").strip()

    if not token:
        print("❌ Error: No token provided.")
        return False

    auth_url = f"https://oauth2:{token}@github.com/VivehaSri/Signova-Sign-Language-detection.git"
    print(f"🚀 Pushing commits to {REMOTE_REPO} (branch: main)...")

    try:
        porcelain.push(REPO_PATH, auth_url, "refs/heads/main:refs/heads/main")
        print("🎉 Successfully pushed all project code to GitHub!")
        print("🔗 View online: https://github.com/VivehaSri/Signova-Sign-Language-detection")
        return True
    except Exception as e:
        print(f"❌ Push failed: {e}")
        return False

if __name__ == "__main__":
    push_repo()
