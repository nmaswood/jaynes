from collections import Counter
from dataclasses import dataclass

from bs4 import BeautifulSoup

from jaynes.email.mbox_utils import read_emails

if False:
    emails = read_emails(limit=100, clean=True)
    froms = [email.from_ for email in emails]
    to = [email.to for email in emails]
    bodies = [email.body for email in emails]
