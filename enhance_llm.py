import os
import json
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path("data/processed")  # where transform.py outputs JSONL
OUTPUT_FILE = DATA_DIR / "jira_dataset.jsonl"

class DummyLLMClient:
    def summarize(self, text: str) -> str:
        return text[:200] + ("..." if len(text) > 200 else "")

    def classify(self, text: str) -> List[str]:
        labels = []
        t = text.lower()
        if "error" in t or "fail" in t or "exception" in t:
            labels.append("bug")
        if "feature" in t or "enhanc" in t:
            labels.append("enhancement")
        if not labels:
            labels.append("other")
        return labels


llm = DummyLLMClient()


def enhance_record(record: Dict) -> Dict:
    combined = record.get("title", "") + "\n" + record.get("description", "")

    if "derived" not in record or not isinstance(record["derived"], dict):
        record["derived"] = {}

    record["derived"]["summary"] = llm.summarize(combined)
    record["derived"]["labels"] = llm.classify(combined)
    return record


def main():
    jsonl_files = list(DATA_DIR.glob("*.jsonl"))
    if not jsonl_files:
        print(f"No JSONL files found in {DATA_DIR}. Run transform.py first.")
        return

    print(f"Enhancing {len(jsonl_files)} JSONL file(s)...")

    for file in jsonl_files:
        enhanced_records = []
        with file.open("r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                enhanced = enhance_record(record)
                enhanced_records.append(enhanced)

        # Save enhanced data
        with OUTPUT_FILE.open("w", encoding="utf-8") as out_f:
            for rec in enhanced_records:
                json.dump(rec, out_f, ensure_ascii=False)
                out_f.write("\n")

    print(f"Enhanced dataset saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
