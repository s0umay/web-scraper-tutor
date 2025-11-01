
## **Overview**


-Fetch: Retrieves public issue data (metadata, comments) from the Jira REST API.
-Transform: Cleans and structures raw JSON data into a clean JSONL format suitable for LLM training.
-Enhance: (Optional) Adds LLM-generated summaries and labels to the dataset.
-Reliable: Designed to be resumable and handle API rate limits, network failures, and data inconsistencies.

## **Setup & Environment**

Install Dependencies It is recommended to use a virtual environment.
- .venv\Scripts\activate
- pip install -r requirements.txt
Configuration Edit config.yaml to set target projects, output directories, and API settings (page size, rate limits).

## **Architecture**
<img width="1536" height="1024" alt="Data Processing Pipeline for Jira Issues" src="https://github.com/user-attachments/assets/0c55dfbf-93e4-4ef9-bef4-b2e9e043e2b9" />
fetch_jira.py → transform.py → enhance_llm.py
1.Fetch: Saves raw JSON issues to data/raw/.
2.Transform: Converts raw JSON to data/processed/jira_dataset.jsonl.
3.Enhance: (Optional) Enriches the dataset and saves to data/processed/jira_dataset_enhanced.jsonl.

#### Key Components:
- fetch_jira.py: Handles API requests, pagination, retries, and checkpointing.
- transform.py: Cleans and structures data, handling missing fields and malformed text.
- enhance_llm.py: Adds derived tasks (e.g., summaries) using a pluggable LLM client.
- validators/schema.py: Pydantic models to ensure data schema consistency.
- run_pipeline.py: Main orchestrator script to run the full pipeline.

## **Reliability & Edge Cases**

* Network Failures: Retries with exponential/randomized backoff.
* Rate Limiting: Detects HTTP 429 and sleeps before retrying.
* Missing Fields: Uses defaults to prevent runtime errors.
* Resumability: Checkpoints allow resuming interrupted fetches.

## **Optimization and Future Improvements**

- Batch Fetching: Configurable page size to reduce API calls.
- Incremental Saving: Saves data issue-by-issue to prevent data loss on failure.
- JSONL Format: Efficient for line-by-line reading of large datasets.

#### In Future I would Like to:
- Integrate real LLM clients (OpenAI, LLaMA).
- Implement parallel/multithreaded fetching.
- Auto-generate more derived tasks

## **USAGE**
1. Run the Pipeline-> python run_pipeline.py
2. Check Outputs
- Raw Data: data/raw/
- Transformed: data/processed/jira_dataset.jsonl
- Enhanced: data/processed/jira_dataset_enhanced.jsonl
3. Validate Data->Use the notebooks/validate_dataset.ipynb notebook to verify the schema and perform exploratory data analysis (EDA) on the generated dataset.
