from pydantic import BaseModel, Field
from typing import List, Optional

class Comment(BaseModel):
    author: Optional[str]
    created: Optional[str]
    body: str

class IssueRecord(BaseModel):
    issue_key: str
    project: str
    title: str
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    labels: List[str] = Field(default=[])
    created: Optional[str]
    updated: Optional[str]
    comments: List[Comment]
    derived: dict
