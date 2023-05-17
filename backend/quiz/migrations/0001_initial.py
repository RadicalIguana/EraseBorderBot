# Generated by Django 4.2 on 2023-05-17 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('chat_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=32, verbose_name='First name')),
                ('last_name', models.CharField(max_length=32, verbose_name='Last name')),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='Phone')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=350, verbose_name='Answer text')),
                ('is_right', models.BooleanField(default=False, verbose_name='Правильный ответ')),
                ('is_clicked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('radio', 'radio'), ('checkbox', 'checkbox'), ('text', 'text')], default='radio', max_length=8)),
                ('text', models.CharField(max_length=350, verbose_name='Question text')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='Subject title')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='Test title')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('result', models.IntegerField()),
                ('all_question', models.IntegerField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('answer', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='question', chained_model_field='question', on_delete=django.db.models.deletion.CASCADE, to='quiz.answer')),
                ('question', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='test', chained_model_field='test', on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.subject')),
                ('test', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='subject', chained_model_field='subject', on_delete=django.db.models.deletion.CASCADE, to='quiz.test')),
            ],
            options={
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.test'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question'),
        ),
    ]
