import re

def parse_article_id(url):
    match = re.search(r'[a-f0-9]{12}$', url)
    return match.group(0) if match else None
