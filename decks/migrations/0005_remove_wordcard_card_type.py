# Generated by Django 4.2.7 on 2023-12-08 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0004_alter_wordcard_deck'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordcard',
            name='card_type',
        ),
    ]
