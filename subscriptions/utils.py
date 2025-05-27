from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_welcome_email(email):
    subject = "Aramıza Hoş Geldin!"
    message = render_to_string("email/welcome.html", {"email": email})
    send_mail(
        subject,
        message,
        "no-reply@searchprojectdemo.com",  # from
        [email],                            # to
        html_message=message
    )
