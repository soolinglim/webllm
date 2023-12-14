# Generated by Django 4.2.7 on 2023-12-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0045_userinput_hide'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunComplete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('session', models.UUIDField(blank=True, default=None, null=True)),
                ('user_input', models.TextField(blank=True)),
                ('iteration', models.IntegerField(blank=True, null=True)),
                ('current_iteration_results', models.TextField(blank=True)),
            ],
        ),
    ]