import smtplib
import ssl
from email.message import EmailMessage
import os
from email_tools import *


def main():
    email_sender = #email address here
    email_password = os.environ.get('PASSWORD')
    email_receiver= #email address here
    subject = 'Your Daily Dashboard'
    body = generate_content()
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

main()
