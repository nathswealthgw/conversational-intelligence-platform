from pydantic import BaseModel, Field
from typing import List


class DocumentIngestRequest(BaseModel):
    source: str = Field(..., example="s3://bucket/documents/hr_policy.pdf")
    content: str = Field(..., example="Document text goes here")


class BatchIngestRequest(BaseModel):
    documents: List[DocumentIngestRequest]
