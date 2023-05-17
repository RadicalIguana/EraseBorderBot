from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.utils.translation import gettext_lazy as _

from smart_selects.db_fields import ChainedForeignKey

class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, chat_id='admin'):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            chat_id=chat_id,
            email=self.normalize_email(email),
            phone=phone
        )

        user.set_password(password)
        # user.set_unusable_password()
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
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    chat_id = models.CharField(max_length=30, primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField('First name', max_length=32)
    last_name = models.CharField('Last name', max_length=32)
    phone = models.CharField('Phone', max_length=12, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email

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
    title = models.CharField("Subject title", max_length=50)
    
    def __str__(self):
        return self.title
    

class Test(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # test_number = models.CharField('Test number', max_length=10)
    title = models.CharField('Test title', max_length=100)
    
    def __str__(self):
        return self.title
    
    
class Question(models.Model):
    
    class TypeChoice(models.TextChoices):
        RADIO = "radio", _("radio")
        CHECKBOX = "checkbox", ("checkbox")
        TEXT = "text", _("text")
    
    id = models.BigAutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=8,
        choices=TypeChoice.choices,
        default=TypeChoice.RADIO
    )
    text = models.CharField('Question text', max_length=255)
    
    def __str__(self):
        return self.text
    

class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField('Answer text', max_length=255)
    is_right = models.BooleanField('Правильный ответ', default=False)
    is_clicked = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
    
    
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
        verbose_name_plural = 'Quizes'
    
    def __str__(self):
        return 'Quiz'
    
    
class Result(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.IntegerField()
    all_question = models.IntegerField()
    
    
class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(max_length=255)
    
