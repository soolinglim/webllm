# Generated by Django 4.2.7 on 2023-11-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0004_rename_image_url_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='elapsed_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
