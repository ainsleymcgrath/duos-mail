import sendgrid
import os


# from sqlalchemy.engine.url import URL
# from sqlalchemy import create_engine, MetaData

SOME_RECIPIENTS = [
    {
        "name": "hilrious!",
        "paper_title": "no way",
        "email": "ainsley.mcgrath@aptitive.com",
    },
    {
        "name": "alright buddy",
        "paper_title": "millions of 'em",
        "email": "mcgrath.ainsley@gmail.com",
    },
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
                "value": "Hello, -author_name-  What's up with your pape called -paper_title- ? ?",
            }
        ],
    }


sg = sendgrid.SendGridAPIClient(apikey=os.environ.get("SENDGRID_API_KEY"))

response = sg.client.mail.send.post(
    request_body=compose_sendgrid_post_body(
        recipients_with_details=SOME_RECIPIENTS, subject="WOW OKAY DUDE"
    )
)
print(response.status_code)
