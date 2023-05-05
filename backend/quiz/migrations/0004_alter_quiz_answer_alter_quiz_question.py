# Generated by Django 4.2 on 2023-05-05 10:35

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_answer_is_clicked_alter_quiz_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='answer',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='question', chained_model_field='question', on_delete=django.db.models.deletion.CASCADE, to='quiz.answer'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='question',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='test', chained_model_field='test', on_delete=django.db.models.deletion.CASCADE, to='quiz.question'),
        ),
    ]
