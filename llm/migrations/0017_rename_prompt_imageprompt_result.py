# Generated by Django 4.2.7 on 2023-11-16 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0016_imageprompt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imageprompt',
            old_name='prompt',
            new_name='result',
        ),
    ]
