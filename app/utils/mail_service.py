import os
import ssl
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

MAIL_PORT = 465

DEBUG_PORT = 8025

SMTP_SERVER = "smtp.gmail.com"

DEBUG_SMTP_SERVER = "localhost"

SENDER_ADDR = os.getenv("OAKFOLIO_APP_MAIL_ADDR")

SENDER_MAIL_PASSWORD = os.getenv("OAKFOLIO_APP_MAIL_CLIENT_PASSWORD")

def build_email_message(to: str, sub: str, content: str):
	msg = EmailMessage()
	msg["to"] = to
	msg["from"] = SENDER_ADDR
	msg["subject"] = sub
	msg.set_content(content)

	return msg

def send_mail(msg, debug=True):
	if debug:
		with smtplib.SMTP(DEBUG_SMTP_SERVER, DEBUG_PORT) as local_mail_server:
			local_mail_server.send_message(msg)

	else:
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(SMTP_SERVER, MAIL_PORT, context=context) as service_mail_server:
			service_mail_server.login(SENDER_ADDR, SENDER_MAIL_PASSWORD)
			service_mail_server.send_message(msg)

def send_email_verification_mail(verification_link, reciepient):
	if not verification_link: return

	subject="Verify your oakfolio account"

	content=f"""
	Welcome to Oakfolio

	Please Verify your email by clicking the link below

	{verification_link}

	This link will expire in 5 minutes
	"""

	message = build_email_message(to=reciepient, sub=subject, content=content)

	send_mail(message)
