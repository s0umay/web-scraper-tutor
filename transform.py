import os
import json
from pathlib import Path
from typing import Dict, Any

RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/processed/jira_dataset.jsonl")
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def safe_text(s: str) -> str:
    if not s:
        return ""
    return "".join(ch for ch in s if ch == "\n" or ch == "\t" or (" " <= ch <= "~") or ord(ch) >= 160)

def transform_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    fields = issue.get("fields", {})
    comments_raw = fields.get("comment", {}).get("comments", [])
    comments = [{"author": c.get("author", {}).get("displayName"),
                 "created": c.get("created"),
                 "body": safe_text(c.get("body"))} for c in comments_raw]

    return {
        "issue_key": issue.get("key"),
        "project": issue.get("key", "").split("-")[0],
        "title": safe_text(fields.get("summary")),
        "description": safe_text(fields.get("description")),
        "status": (fields.get("status") or {}).get("name"),
        "priority": (fields.get("priority") or {}).get("name"),
        "labels": fields.get("labels", []),
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "comments": comments,
        "derived": {"summary": None, "qa_pairs": []},
        "raw_fields": fields
    }

def main():
    files = list(RAW_DIR.glob("*.json"))
    print(f"Found {len(files)} raw issue files.")
    with OUT_FILE.open("w", encoding="utf-8") as out_f:
        for fpath in files:
            with fpath.open("r", encoding="utf-8") as f:
                issue = json.load(f)
                transformed = transform_issue(issue)
                json.dump(transformed, out_f, ensure_ascii=False)
                out_f.write("\n")
    print(f"Transformed data saved to {OUT_FILE}")

if __name__ == "__main__":
    main()