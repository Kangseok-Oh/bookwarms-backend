# Generated by Django 5.0.4 on 2024-04-27 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('category_big_name', models.CharField(max_length=20)),
                ('category_sml_name', models.CharField(max_length=20)),
            ],
        ),
    ]
