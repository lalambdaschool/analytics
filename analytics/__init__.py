import os
import re
import sys
from datetime import datetime, timedelta

import gspread
from pyrogram import Client
from pyrogram.types import ChatEventFilter

api_id = os.environ["TELEGRAM_API_ID"]
api_hash = os.environ["TELEGRAM_API_HASH"]
session_string = os.environ["TELEGRAM_SESSION_STRING"]

channel_username = "lalambdaschool"
to_date = datetime.now() - timedelta(days=30)

gc = gspread.oauth(
    credentials_filename="./client_secret.json",
    authorized_user_filename="./authorized_user.json",
)
registrations = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/149pgsbW9WTarfdjIG22nr6bbRsMCMfGfWNlhadH_6CI"
).get_worksheet(0)
nicknames = registrations.col_values(12)[1:]
nicknames = set(map(lambda x: re.findall(r"\w+", x)[-1], nicknames))

with Client(
    "my_account", api_id, api_hash, session_string=session_string, ipv6=True
) as client:
    # Get the number of chat members
    members_count = client.get_chat_members_count(channel_username)

    # Get the chat members
    chat_members = client.get_chat_members(channel_username, limit=members_count)

    recent_members = filter(lambda x: x.joined_date > to_date, chat_members)

    unregistered_members = filter(
        lambda x: x.user.username not in nicknames, recent_members
    )

    for member in unregistered_members:
        print(f"@{member.user.username} ({member.joined_date})")
