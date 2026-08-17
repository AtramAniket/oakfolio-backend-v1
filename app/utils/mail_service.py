import os
import smtplib
from brevo import AsyncBrevo
from app.core.config import settings
from email.message import EmailMessage
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)


DEBUG_PORT = 8025
DEBUG_SMTP_SERVER = "localhost"

BREVO_API_KEY = settings.brevo_api_key
SENDER_ADDR = settings.oakfolio_app_mail_addr

brevo_client = AsyncBrevo(api_key=BREVO_API_KEY)


def build_email_message(to: str, sub: str, content: str):
    msg = EmailMessage()

    msg["to"] = to
    msg["from"] = SENDER_ADDR
    msg["subject"] = sub

    msg.set_content(content)

    return msg


async def send_mail(msg, debug=True):

    if debug:
        with smtplib.SMTP(
            DEBUG_SMTP_SERVER,
            DEBUG_PORT
        ) as local_mail_server:

            local_mail_server.send_message(msg)

    else:
        result = await brevo_client.transactional_emails.send_transac_email(
            sender=SendTransacEmailRequestSender(
                email=msg["from"],
                name="Oakfolio",
            ),
            to=[
                SendTransacEmailRequestToItem(
                    email=msg["to"],
                )
            ],
            subject=msg["subject"],
            text_content=msg.get_content(),
        )

        return result


async def send_email_verification_mail(
    verification_link,
    reciepient,
    debug=False,
):

    if not verification_link:
        return

    subject = "Verify your Oakfolio account"

    content = f"""
	Welcome to Oakfolio

	Please verify your email by clicking the link below:

	{verification_link}

	This link will expire in 5 minutes.
	"""

    message = build_email_message(
        to=reciepient,
        sub=subject,
        content=content,
    )

    await send_mail(
        message,
        debug=debug,
    )