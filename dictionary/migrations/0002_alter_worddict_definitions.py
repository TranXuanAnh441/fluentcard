# Generated by Django 4.2.6 on 2023-10-15 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worddict',
            name='definitions',
            field=models.CharField(max_length=5000),
        ),
    ]