from dataclasses import dataclass
from typing import List, Union


@dataclass
class Text:
    content: str


@dataclass
class Image:
    src: str
    alt: str
    width: int
    height: int


@dataclass
class Paragraph:
    children: List[Union[Text, Image]]


@dataclass
class Page:
    title: str
    author: str
    created_at: str
    content: List[Paragraph]
