import re


def parse_article_id(url):
    matches = re.findall(r"([a-f0-9]{12})(?=[/?#]?($|[?#/]))", url)
    return matches[-1][0] if matches else None
