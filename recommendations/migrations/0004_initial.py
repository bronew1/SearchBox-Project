# Generated by Django 5.1.1 on 2025-06-02 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recommendations', '0003_delete_userinteraction'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartAbandonment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('product_id', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('purchased', models.BooleanField(default=False)),
            ],
        ),
    ]
