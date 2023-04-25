import os
from typing import List

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


templates = {
    'sing_up': './templates/sing_up.html',
    'recovery_password': './templates/recovery_password.html'
}


def get_email_template(template_name: str):
    template_path = templates[template_name]
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content


async def send_email(recipients: List[str], subject: str, template: str):
    config_email = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_PORT=os.getenv("MAIL_PORT"),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_TLS=True,
        MAIL_SSL=False
    )

    message = MessageSchema(
        subject=subject,
        recipients=recipients,  # List of recipients, as many as you can pass
        body=template,  # String HTML, content of email
        subtype="html"
    )

    fm = FastMail(config_email)
    await fm.send_message(message)
