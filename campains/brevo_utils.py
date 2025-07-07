import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.BREVO_API_KEY

def send_brevo_email(subject, html_content, to_email):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "no-reply@seninsite.com", "name": "Senin Markan"},
        subject=subject,
        html_content=html_content,
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print(f"Brevo API hatası: {e}")
