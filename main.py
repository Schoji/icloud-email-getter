from imap_tools import MailBox, AND
from dotenv import load_dotenv
from typing import TypedDict
import unicodedata
import os
import re
from urllib.parse import unquote

load_dotenv()

def clean_text(text: str | None) -> str:
    if not text:
        return ""
    # 1. Normalize Unicode (converts non-breaking spaces and other weird variants)
    text = unicodedata.normalize("NFKC", text)
    # 2. Decode %20 etc. (percent-encoding from URLs)
    text = unquote(text)
    # 3. Unify line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 4. Remove invisible / zero-width characters
    text = re.sub(r"[\u200b\u200c\u200d\ufeff\u00ad]", "", text)
    # 5. Collapse non-breaking spaces and other odd whitespace into a single space
    text = re.sub(r"[^\S\n]+", " ", text)   # any whitespace except \n -> space
    # 6. Reduce multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 7. Strip trailing spaces at line ends
    text = re.sub(r" +\n", "\n", text)
    return text.strip()

class Email(TypedDict):
    date: str
    subject: str
    content: str
    from_: str

def main():
    # Get date, subject and body len of all emails from INBOX folder
    ICLOUD_PASSWORD = os.environ.get("ICLOUD_PASSWORD")
    ICLOUD_EMAIL = os.environ.get("ICLOUD_EMAIL")
    if ICLOUD_PASSWORD is None or ICLOUD_EMAIL is None:
        print("Environment variables are not set!")
        return
    
    email_list:list[Email] = []
    
    with MailBox('imap.mail.me.com').login(ICLOUD_EMAIL, ICLOUD_PASSWORD) as mailbox:
        for msg in mailbox.fetch(AND(seen=False),mark_seen=True, bulk=True):
        # for msg in mailbox.fetch(mark_seen=True, bulk=True):
            email: Email = {
                "date": msg.date_str,
                "subject": msg.subject,
                "content": clean_text(msg.text),
                "from_": msg.from_,
            }
            email_list.append(email)
                
    num_emails = len(email_list)
    if num_emails == 0:
        print("No new emails.")
    else:
        print(email_list)

if __name__ == "__main__":
    main()
