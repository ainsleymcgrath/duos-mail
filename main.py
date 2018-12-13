import sendgrid
import os


# from sqlalchemy.engine.url import URL
# from sqlalchemy import create_engine, MetaData

SOME_RECIPIENTS = [
    {
        "name": "Arbus",
        "paper_title": "Flarbus",
        "email": "ainsley.mcgrath@aptitive.com",
    },
    {"name": "Blumbos", "paper_title": "bambu!", "email": "mcgrath.ainsley@gmail.com"},
]


def compose_sendgrid_post_body(recipients_with_details=[], subject=""):
    return {
        "personalizations": [
            {
                "to": [{"email": recipient["email"]}],
                "subject": subject,
                "substitutions": {
                    "-author_name-": recipient["name"],
                    "-paper_title-": recipient["paper_title"],
                },
            }
            for recipient in recipients_with_details
        ],
        "from": {"email": "test@example.com"},
        "content": [
            {
                "type": "text/plain",
                "value": "Hello, -author_name-,\nWhat's up with your pape called -paper_title-??",
            }
        ],
    }


sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))

print(compose_sendgrid_post_body(SOME_RECIPIENTS))

response = sg.client.mail.send.post(
    request_body=compose_sendgrid_post_body(
        recipients_with_details=SOME_RECIPIENTS, subject="awesome test"
    )
)
print(response.status_code)
