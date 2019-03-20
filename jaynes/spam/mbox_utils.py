import mailbox
from dataclasses import dataclass
from datetime import datetime
from typing import Set

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


def list_files(mail_dir):
    pass


def message_body(message: mailbox.mboxMessage) -> _ParsedEmailInfo:

    charsets: Set[str] = set()

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


def read_message_body(message: mailbox.mboxMessage) -> str:
    parsed_email_info = message_body(message)
    charsets = parsed_email_info.charsets
    body = parsed_email_info.body
    charsets.remove(None)  # noqa

    for charset in parsed_email_info.charsets:
        try:
            return parsed_email_info.body.decode(charset)
        except Exception as e:
            print(e)
    else:
        return ' '.join(map(str, body))
