# Generated by Django 4.2.7 on 2023-11-23 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roleplay', '0004_wordusehistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordusehistory',
            name='prompt',
        ),
    ]