# Generated by Django 5.1.1 on 2025-06-01 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_emailtemplatewelcome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplatewelcome',
            name='html_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
