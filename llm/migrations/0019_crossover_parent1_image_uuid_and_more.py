# Generated by Django 4.2.7 on 2023-11-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0018_rename_prompt_userinput'),
    ]

    operations = [
        migrations.AddField(
            model_name='crossover',
            name='parent1_image_uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crossover',
            name='parent2_image_uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
