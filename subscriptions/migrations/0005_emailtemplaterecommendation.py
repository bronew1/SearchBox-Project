# Generated by Django 5.1.1 on 2025-06-20 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_emailtemplatecartreminder'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplateRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('subject', models.CharField(max_length=200)),
                ('html_content', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='email_images/')),
            ],
        ),
    ]
