# Generated by Django 4.2 on 2023-05-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_myuser_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='is_right',
            field=models.BooleanField(default=False, verbose_name='Правильный ответ'),
        ),
    ]