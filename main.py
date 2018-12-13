#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sendgrid
import os

from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, MetaData, select

from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
    ForeignKey,
)

connstr = URL(
    **{
        "drivername": "postgres",
        "username": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME"),
    }
)
engine = create_engine(connstr)
metadata = MetaData()
metadata.reflect(bind=engine)
conn = engine.connect()

wr = metadata.tables["writes"]
ar = metadata.tables["article"]
au = metadata.tables["author"]

join = wr.join(au, au.c.author_id == wr.c.author_id).join(
    ar, ar.c.article_id == wr.c.article_id
)

result = conn.execute(
    select(
        [ar.c.article_title, wr.c.writes_hash, au.c.author_name, au.c.email_address]
    ).select_from(join)
)


def iter_make_recipient(recipient_iterable):
    for recipient in recipient_iterable:
        yield {
            "paper_title": recipient[0],
            "url_hash": recipient[1],
            "name": recipient[2],
            "email": recipient[3],
        }


def compose_sendgrid_post_body(recipients_with_details=[], subject="", from_email=""):
    return {
        "personalizations": [
            {
                "to": [{"email": recipient["email"]}],
                "subject": subject,
                "substitutions": {
                    "-author_name-": recipient["name"],
                    "-paper_title-": recipient["paper_title"],
                    "-url_hash-": recipient["url_hash"],
                },
            }
            for recipient in recipients_with_details
        ],
        "from": {"email": from_email},
        "content": [
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
                for record in iter_make_recipient(result.fetchall())
                if record["email"] is not None
            ],
            "subject": "WOW OKAY DUDE",
            "from_email": "test@example.com",
        }
    )
)
print(response.status_code)
