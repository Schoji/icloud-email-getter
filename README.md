# 📬 icloud-email-getter

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/managed%20with-uv-DE5FE9?logo=uv&logoColor=white)
![imap-tools](https://img.shields.io/badge/imap--tools-1.13+-2C8EBB)
![IMAP](https://img.shields.io/badge/protocol-IMAP-orange)
![Platform](https://img.shields.io/badge/mailbox-iCloud-000000?logo=icloud&logoColor=white)
![Status](https://img.shields.io/badge/status-WIP-yellow)

A small Python script that connects to an iCloud mailbox over IMAP, fetches
messages from the inbox, and cleans up their text (removing `\r\n`, `%20`,
non-breaking spaces and other invisible characters) into tidy `Email` records.

## Requirements

- Python >= 3.12
- An iCloud **app-specific password** (a regular Apple ID password will not work
  with IMAP). Generate one at <https://account.apple.com> → *Sign-In and Security*
  → *App-Specific Passwords*.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync
```

Create a `.env` file in the project root with your iCloud address and
app-specific password:

```env
ICLOUD_EMAIL=your-address@icloud.com
ICLOUD_PASSWORD=your-app-specific-password
```

> The IMAP host is fixed to `imap.mail.me.com` (iCloud) in `main.py`.

## Usage

```bash
uv run main.py
```

The script logs in, fetches the messages, prints the resulting list of `Email`
records, or `No new emails.` if the inbox has none.

## How it works

- Loads `ICLOUD_EMAIL` and `ICLOUD_PASSWORD` from `.env` via `python-dotenv`.
- Connects to `imap.mail.me.com` using [`imap-tools`](https://github.com/ikvk/imap_tools).
- For each message, builds a typed `Email` dict with `date`, `subject`,
  `content`, and `from_`.
- `clean_text()` normalizes the message body:
  - Unicode NFKC normalization (fixes non-breaking spaces and odd variants)
  - decodes percent-encoding (`%20` → space)
  - unifies line endings and trims stray whitespace
  - strips zero-width / invisible characters

## Project structure

```
main.py          # entry point: fetch + clean emails
pyproject.toml   # project metadata and dependencies
.env             # ICLOUD_PASSWORD (not committed)
```
