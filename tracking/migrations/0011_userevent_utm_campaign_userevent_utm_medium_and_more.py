# Generated by Django 5.1.1 on 2025-07-08 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0010_userevent_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='userevent',
            name='utm_campaign',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userevent',
            name='utm_medium',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userevent',
            name='utm_source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
