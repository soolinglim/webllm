# Generated by Django 4.2.7 on 2023-11-24 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0028_crossover_iteration_image_iteration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSelectionFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('session', models.UUIDField(blank=True, default=None, null=True)),
                ('iteration', models.IntegerField(blank=True, null=True)),
                ('parent_1', models.CharField(blank=True, max_length=8)),
                ('parent_1_json', models.TextField(blank=True)),
                ('parent_1_feedback', models.TextField(blank=True)),
                ('parent_2', models.CharField(blank=True, max_length=8)),
                ('parent_2_json', models.TextField(blank=True)),
                ('parent_2_feedback', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='instance',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AddField(
            model_name='imageprompt',
            name='instance',
            field=models.CharField(blank=True, max_length=8),
        ),
    ]
