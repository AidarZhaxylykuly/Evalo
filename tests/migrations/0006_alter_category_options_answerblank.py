# Generated by Django 5.1.1 on 2024-10-22 21:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_alter_test_starting_datetime_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='AnswerBlank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Answers', models.JSONField(default=dict)),
                ('Score', models.FloatField()),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('Test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blank_test', to='tests.test')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blank_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AnswerBlank',
                'verbose_name_plural': 'AnswerBlanks',
            },
        ),
    ]