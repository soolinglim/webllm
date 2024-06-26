# Generated by Django 4.2.7 on 2023-11-10 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0009_prompt_elapsed_time_prompt_end_time_prompt_response_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crossover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('json1', models.TextField(blank=True)),
                ('json2', models.TextField(blank=True)),
                ('response', models.TextField(blank=True)),
                ('result', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('elapsed_time', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
