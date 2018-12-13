#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""run as a scheduled heroku job to send out emails 
for the duos research study"""


import sendgrid
import os

from db import fetch_email_recipients
from plumbing import compose_sendgrid_post_body, iter_make_recipient


CONSTANTS = {
    "SUBJECT": "WOW OKAY DUDE",
    "FROM_EMAIL": "yooo@example.com",
    "CONTENT": [
        {
            "type": "text/plain",
            "value": "Hello, -author_name-  What's up with your paper called -paper_title- answer my question at -url_hash-",
        }
    ],
}

sg = sendgrid.SendGridAPIClient(apikey=os.getenv("SENDGRID_API_KEY"))

response = sg.client.mail.send.post(
    request_body=compose_sendgrid_post_body(
        **{
            "recipients_with_details": [
                record
                for record in iter_make_recipient(fetch_email_recipients())
                if record["email"] is not None
            ],
            "subject": CONSTANTS["SUBJECT"],
            "from_email": CONSTANTS["FROM_EMAIL"],
            "content": CONSTANTS["CONTENT"],
        }
    )
)

print(f"{'Success 🙌' if response.status_code == 202 or 200 else 'Uh oh 🙀'}")
print(f"Response code: {response.status_code}")
