import os, subprocess, yaml, sys

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

os.makedirs(cfg.get("outdir","data"), exist_ok=True)

PY = sys.executable   # ✅ ensures it uses current venv Python

print("1) Fetching raw Jira issues...")
subprocess.run([PY, "fetch_jira.py"], check=True)

print("2) Transforming...")
subprocess.run([PY, "transform.py"], check=True)

print("3) Enhancing with LLM...")
subprocess.run([PY, "enhance_llm.py"], check=True)

print("✅ Done.")
