#!/usr/bin/env python3
# This script retrieves the list of changed files in a pull request and filters for those under the "force-app/" directory that are not removed. 
# It is used in the pr-validate-deploy workflow to determine which metadata files need to be included in the validation deployment manifest.
# Right now it ignores removed files.  However, we can likely dynamically build the destructive changes manifest in the future based on removed files if desired.
import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    pr_number = os.environ.get("PR_NUMBER", "").strip()
    token = os.environ.get("GITHUB_TOKEN", "").strip()

    if not repo or not pr_number or not token:
        print("Missing required environment variables: GITHUB_REPOSITORY, PR_NUMBER, GITHUB_TOKEN", file=sys.stderr)
        return 1

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files?per_page=100"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    changed_paths: list[str] = []

    while url:
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request) as response:
                body = response.read().decode("utf-8")
                files = json.loads(body)

                for file_item in files:
                    status = file_item.get("status", "")
                    filename = file_item.get("filename", "")
                    if not filename.startswith("force-app/"):
                        continue
                    if status == "removed":
                        continue
                    changed_paths.append(filename)

                link_header = response.headers.get("Link", "")
                next_url = None
                for part in link_header.split(","):
                    part = part.strip()
                    if 'rel="next"' in part:
                        next_url = part.split(";")[0].strip().strip("<>")
                        break
                url = next_url
        except urllib.error.HTTPError as error:
            print(f"GitHub API request failed with status {error.code}", file=sys.stderr)
            return 1

    for path in changed_paths:
        print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
