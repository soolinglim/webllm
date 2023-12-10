# Generated by Django 4.2.7 on 2023-11-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0013_mutation'),
    ]

    operations = [
        migrations.AddField(
            model_name='crossover',
            name='parent1_image_uuid',
            field=models.UUIDField(default='b30573e1-b3af-40ae-9583-346683d27ac9'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crossover',
            name='parent2_image_uuid',
            field=models.UUIDField(default='030e6cd8-d336-47ce-a73c-fa516e012e83'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='uuid',
            field=models.UUIDField(default='030e6cd8-d336-47ce-a73c-fa516e012e83'),
            preserve_default=False,
        ),
    ]
