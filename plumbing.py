"""helper functions"""


def iter_make_recipient(recipient_iterable):
    """parse the tuples of a sqlalchemy result set into an iterable of dicts"""
    for recipient in recipient_iterable:
        yield {
            "paper_title": recipient[0],
            "url_hash": recipient[1],
            "name": recipient[2],
            "email": recipient[3],
        }


def compose_sendgrid_post_body(
    recipients_with_details=[], subject="", from_email="", content=[{}]
):
    """build the request body for a post to the /mail/send endpoint of Sendgrid"""
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
        "content": content,
    }
