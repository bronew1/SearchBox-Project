# Generated by Django 5.1.1 on 2025-06-27 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0008_rename_email_sent_cartabandonment_is_email_sent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PushSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.TextField()),
                ('keys_auth', models.CharField(max_length=256)),
                ('keys_p256dh', models.CharField(max_length=256)),
                ('user_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
