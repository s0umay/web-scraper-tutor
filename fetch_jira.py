import os
import json
import time
import random
from typing import Optional, Dict, Any, List
import requests
import yaml

CONFIG_PATH = "config.yaml"
BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"

def safe_text(s: Optional[str]) -> str:
    if s is None:
        return ""
    return ''.join(ch for ch in s if (ch == "\n" or ch == "\t" or (" " <= ch <= "~") or ord(ch) >= 160))

def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def fetch_issues(project: str, start_at: int, max_results: int, retries: int) -> List[Dict[str, Any]]:
    params = {
        "jql": f"project={project}",
        "startAt": start_at,
        "maxResults": max_results,
        "fields": "*all"
    }
    attempt = 0
    while attempt <= retries:
        try:
            resp = requests.get(BASE_URL, params=params, timeout=20)
            if resp.status_code == 429:
                sleep_time = 5 + random.random() * 5
                print(f"Rate limited, sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                attempt += 1
                continue
            resp.raise_for_status()
            data = resp.json()
            return data.get("issues", [])
        except Exception as e:
            print(f"Fetch error: {e}, retrying...")
            time.sleep(2 + random.random() * 3)
            attempt += 1
    return []

def save_checkpoint(project: str, start_at: int, outdir: str):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, f"{project}_checkpoint.json"), "w") as f:
        json.dump({"start_at": start_at}, f)

def load_checkpoint(project: str, outdir: str) -> int:
    path = os.path.join(outdir, f"{project}_checkpoint.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f).get("start_at", 0)
    return 0

def main():
    cfg = load_config()
    projects = cfg.get("projects", [])
    outdir = cfg.get("outdir", "./data/raw")
    page_size = cfg.get("page_size", 50)
    max_results = cfg.get("max_results", 200)
    retries = cfg.get("rate_limit", {}).get("max_retries", 5)

    os.makedirs(outdir, exist_ok=True)

    for project in projects:
        print(f"Scraping project: {project}")
        start_at = load_checkpoint(project, outdir)
        total_fetched = 0

        while True:
            issues = fetch_issues(project, start_at, page_size, retries)
            if not issues:
                break
            for issue in issues:
                key = issue.get("key")
                filepath = os.path.join(outdir, f"{key}.json")
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(issue, f, ensure_ascii=False)
            start_at += len(issues)
            save_checkpoint(project, start_at, outdir)
            total_fetched += len(issues)
            print(f"Fetched {total_fetched} issues for {project}")
            if start_at >= max_results:
                break
            time.sleep(random.uniform(0.5, 1.5))
        print(f"Completed scraping {project}")

if __name__ == "__main__":
    main()