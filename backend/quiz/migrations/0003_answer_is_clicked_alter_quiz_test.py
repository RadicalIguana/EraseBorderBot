# Generated by Django 4.2 on 2023-05-04 10:42

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_clicked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='test',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='subject', chained_model_field='subject', on_delete=django.db.models.deletion.CASCADE, to='quiz.test'),
        ),
    ]
