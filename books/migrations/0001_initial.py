# Generated by Django 5.0.4 on 2024-04-27 06:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_isbn', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=100)),
                ('book_price', models.PositiveIntegerField()),
                ('book_intro', models.TextField(blank=True, max_length=3000, null=True)),
                ('book_contents', models.TextField(blank=True, max_length=500, null=True)),
                ('book_total_words', models.CharField(blank=True, max_length=5, null=True)),
                ('book_publisher', models.CharField(max_length=50)),
                ('book_interpreter', models.CharField(max_length=50)),
                ('book_cover_path', models.URLField(blank=True, null=True)),
                ('book_ebook_path', models.URLField()),
                ('book_author_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authors.author')),
                ('book_category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category')),
            ],
        ),
    ]