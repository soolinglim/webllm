# Generated by Django 4.2.7 on 2023-11-16 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0015_remove_crossover_parent1_image_uuid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_input', models.TextField(blank=True)),
                ('attributes', models.TextField(blank=True)),
                ('response', models.TextField(blank=True)),
                ('prompt', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('elapsed_time', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
