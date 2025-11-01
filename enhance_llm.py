import os
import json
import time
from typing import List, Dict
import yaml


CONFIG_PATH = 'config.yaml'


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        
        return yaml.safe_load(f)


class DummyLLMClient:
    def summarize(self, text: str) -> str:
        return text[:200] + ('...' if len(text) > 200 else '')

    def classify(self, text: str) -> List[str]:
        labels = []
        t = text.lower()
        if 'error' in t or 'fail' in t or 'exception' in t:
            labels.append('bug')
        if 'feature' in t or 'enhanc' in t:
            labels.append('enhancement')
        if not labels:
            labels.append('other')
        return labels



llm = DummyLLMClient()


def enhance_record(record: Dict) -> Dict:
    combined = record.get('title','') + '\n' + record.get('description','')
    summary = llm.summarize(combined)
    labels = llm.classify(combined)

    if 'derived' not in record or not isinstance(record['derived'], dict):
        record['derived'] = {}

    record['derived']['summary'] = summary
    record['derived']['labels'] = labels
    return record



if __name__ == '__main__':
    print('Run via run_pipeline.py to process all files in data/processed')