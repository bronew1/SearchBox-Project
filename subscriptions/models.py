# subscriptions/models.py
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# subscriptions/models.py

from django.db import models

from django.db import models

class EmailTemplateWelcome(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    html_content = models.TextField(blank=True, null=True)  # Artık zorunlu değil
    image = models.ImageField(upload_to='email_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class EmailTemplateCartReminder(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    html_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='email_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class EmailTemplateRecommendation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    html_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='email_images/', blank=True, null=True)

    def __str__(self):
        return self.name
