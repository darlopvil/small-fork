from dataclasses import dataclass
from datetime import datetime


@dataclass
class Page:
    title: str
    author: str
    created_at: datetime
    content: str
