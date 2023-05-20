from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from smart_selects.db_fields import ChainedForeignKey

class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, chat_id='admin'):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if email == "":
            email = None
            
        user = self.model(
            chat_id=chat_id,
            email=self.normalize_email(email),
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            chat_id = 'admin',
            password=password,
            phone=phone
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    chat_id = models.CharField(max_length=30, primary_key=True)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        null=True,
        unique=True,
        blank=True,
        default=None
    )
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32)
    phone = models.CharField('Номер телефона', max_length=12, null=True, unique=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField('Администратор', default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.email == "":
            self.email = None
        if self.phone == "":
            self.phone = None
        super(MyUser, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Subject(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField("Предмет", max_length=50)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Предметы"
    

class Test(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, verbose_name="Предмет" , on_delete=models.CASCADE)
    # test_number = models.CharField('Test number', max_length=10)
    title = models.CharField('Тест', max_length=100)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Тесты"
    
    
class Question(models.Model):
    
    class TypeChoice(models.TextChoices):
        RADIO = "radio", _("radio")
        CHECKBOX = "checkbox", ("checkbox")
        TEXT = "text", _("text")
    
    id = models.BigAutoField(primary_key=True)
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)
    type = models.CharField(
        max_length=8,
        choices=TypeChoice.choices,
        default=TypeChoice.RADIO
    )
    text = models.CharField('Вопросы', max_length=350)
    
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name_plural = "Вопросы"
    

class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, verbose_name='Вопрос' , on_delete=models.CASCADE)
    text = models.CharField('Ответ', max_length=350)
    is_right = models.BooleanField('Правильный ответ?', default=False)
    # is_clicked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name_plural = "Ответы"
    
    
class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = ChainedForeignKey(
        Test, 
        chained_field = 'subject',
        chained_model_field = 'subject',
        show_all = False,
        auto_choose = True,
        sort = True,
        on_delete=models.CASCADE
    )
    question = ChainedForeignKey(
        Question,
        chained_field = 'test',
        chained_model_field = 'test',
        show_all = False,
        auto_choose = True,
        sort = True,
        on_delete=models.CASCADE
    )
    answer = ChainedForeignKey(
        Answer,
        chained_field = 'question',
        chained_model_field = 'question',
        show_all = False,
        auto_choose = True,
        sort = True,
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name_plural = 'Викторины'
    
    def __str__(self):
        return 'Quiz'
    
    @admin.display(description='Subject')
    def quiz_subject(self):
        subject = Subject.objects.get(id=self.subject.id)
        subject_title = subject.title
        return f"{subject_title}"
    
    
class Result(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(MyUser, verbose_name='Пользовательское ID', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)
    result = models.IntegerField()
    all_question = models.IntegerField()
    
    @admin.display(description="Имя")
    def first_name(self):
        first_name = self.user.first_name
        return f"{first_name}"
    
    @admin.display(description="Фамилия")
    def last_name(self):
        last_name = self.user.last_name
        return f"{last_name}"
    
    @admin.display(description="Результат")
    def total_result(self):
        return f"{self.result} / {self.all_question}"
    
    class Meta:
        verbose_name_plural = "Результаты"
    
    
class Feedback(models.Model):
    id = models.BigAutoField(verbose_name='#', primary_key=True)
    text = models.TextField(verbose_name='Текст', max_length=255)
    
    class Meta:
        verbose_name_plural = "Обратная связь"
    
