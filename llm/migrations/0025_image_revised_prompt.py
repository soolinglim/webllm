# Generated by Django 4.2.7 on 2023-11-22 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0024_mutation_mutation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='revised_prompt',
            field=models.TextField(blank=True),
        ),
    ]
