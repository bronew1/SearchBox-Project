from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_welcome_email(email):
    subject = "Aramıza Hoş Geldin!"
    message = render_to_string("email/welcome.html", {"email": email})
    send_mail(
        subject,
        message,
        "8e19eb003@smtp-brevo.com",  # From bu olmalı!
        [email],
        html_message=message
    )
