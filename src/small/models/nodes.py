from dataclasses import dataclass
from typing import List, Union


@dataclass
class Text:
    content: str
    type: str


@dataclass
class Image:
    src: str
    alt: str
    width: int
    height: int


@dataclass
class IFrame:
    src: str
    width: int
    height: int


@dataclass
class GithubGist:
    id: str
    filename: str = None
    content: str = None


@dataclass
class Paragraph:
    children: List[Union[Text, Image, IFrame, GithubGist]]


@dataclass
class Page:
    title: str
    author: str
    created_at: str
    content: List[Paragraph]
