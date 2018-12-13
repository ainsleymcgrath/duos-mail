"""consolidation of database i/o"""


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


def fetch_email_recipients():
    """indiscriminately grab email addresses 
    and data for email bodies from the database"""
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

    return result.fetchall()
