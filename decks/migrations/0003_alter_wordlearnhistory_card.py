# Generated by Django 4.2.6 on 2023-10-21 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0002_remove_wordcard_content_alter_wordcard_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordlearnhistory',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_learn_history', to='decks.wordcard'),
        ),
    ]