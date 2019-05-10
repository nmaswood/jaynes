import re

from bs4 import BeautifulSoup


def strip_non_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for s in soup(['script', 'style']):
        s.decompose()
    return ' '.join(soup.stripped_strings)


def clean_text(text):

    text = text.lower()
    text = re.sub(r"\s+", ' ', text).strip()
    text = re.sub(r'\.{5,}', '', text)
    text = re.sub(r'\*{5,}', '', text)
    text = re.sub(r'-{5,}', '', text)
    text = re.sub(r'_{5,}', '', text)
    text = re.sub(r'(\d{1,3} \d{1,3}){1,}', '', text)

    return text
