import json
import mailbox
import os
import re
from dataclasses import dataclass
from datetime import datetime
from glob import glob
from typing import Any, Dict, List, Set
from uuid import uuid4

from bs4 import BeautifulSoup
from dateutil.parser import parse

import jaynes.text_utils as text_utils
from jaynes.constants import DERIVED_DIR, ROOT_DIR

MAIL_DIR = 'Mail'


@dataclass
class _ParsedEmailInfo:
    body: bytes
    charsets: Set[str]


@dataclass
class Email:
    id: str
    label: str
    date: datetime
    subject: str
    from_: str
    to: str
    body: str


def from_json(json_dict: Dict[str, Any]) -> Email:
    date = json_dict["date"]
    return Email(
        json_dict["id"],
        json_dict["label"],
        parse(date) if date else None,
        json_dict["subject"],
        json_dict["from_"],
        json_dict["to"],
        json_dict["body"],
    )


def _parsed_email_info(message: mailbox.mboxMessage) -> _ParsedEmailInfo:

    charsets: Set[str] = set()

    body = b''
    if not message.is_multipart():
        body = message.get_payload(decode=True)
        charsets.update(message.get_charsets())
        return _ParsedEmailInfo(body, charsets)

    for part in message.walk():
        if part.is_multipart():

            for subpart in part.walk():
                if subpart.get_content_type() == 'text/plain':
                    body = subpart.get_payload(decode=True)
                    break

        elif part.get_content_type() == 'text/plain':
            body = message.get_payload(decode=True)
            break

    return _ParsedEmailInfo(body, charsets)


def message_body(message: mailbox.mboxMessage) -> str:
    parsed_email_info = _parsed_email_info(message)
    charsets = parsed_email_info.charsets
    body = parsed_email_info.body

    if None in charsets:
        charsets.remove(None)  # noqa

    for charset in parsed_email_info.charsets:
        try:
            return parsed_email_info.body.decode(charset)
        except Exception as e:
            print(e)
    else:
        if not body:
            return ''
        return ' '.join(map(str, body))


def from_email(message: mailbox.mboxMessage, label: str = None) -> Email:
    body = message_body(message)

    if label is None:
        labels = message.get('X-Gmail-Labels', '')
        label = labels.split(',')[0]

    date = message.get('Date')
    subject = message.get('Subject')
    from_ = message.get('From')
    to = message.get('To')
    id_ = message.get('Message-Id')

    return Email(
        id_,
        label,
        date,
        subject,
        from_,
        to,
        body,
    )


def get_label(file_name):
    return file_name.rsplit('/', 1)[-1].strip('.mbox')


def process_emails() -> List[Email]:
    path = os.path.join(ROOT_DIR, MAIL_DIR, '*.mbox')
    email_paths = glob(path)
    emails: List[Email] = []
    for email_path in email_paths:
        mboxs = mailbox.mbox(email_path)
        for mbox in mboxs:
            email = from_email(mbox)

            emails.append(email)
    return emails


def write_emails(dir_: str, emails: List[Email]) -> None:
    for email in emails:
        path = os.path.join(dir_, '{}.json'.format(uuid4()))
        with open(path, 'w') as outfile:
            json.dump(email.__dict__, outfile)


def read_emails(dir_: str = DERIVED_DIR,
                limit=float('inf'),
                clean: bool = True) -> List[Email]:
    emails: List[Email] = []
    files = glob('{}/*.json'.format(dir_))
    for idx, file_ in enumerate(files):
        with open(file_, 'r') as infile:
            email = json.load(infile)
            if clean:

                text = text_utils.strip_non_content(email['body'])
                text = text_utils.clean_text(text)
                email['body'] = text

            email_object = from_json(email)
            emails.append(email_object)

        if idx == limit:
            break
    return emails


if __name__ == '__main__':

    emails = process_emails()
    write_emails(DERIVED_DIR, emails)
