# Generated by Django 4.2.7 on 2023-11-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0031_rename_parent1_userselectionfeedback_parent1_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInputInitial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('session', models.UUIDField(blank=True, default=None, null=True)),
                ('iteration', models.IntegerField(blank=True, null=True)),
                ('user_input', models.TextField(blank=True)),
            ],
        ),
    ]