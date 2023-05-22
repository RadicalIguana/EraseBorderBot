from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from django.urls import path, reverse
from django.views.generic.detail import DetailView
from django.utils.html import format_html

from .models import Subject, Test, Question, Answer, Quiz, MyUser, Result, Feedback

class MyUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'fields': ('email', 'date_of_birth', 'password1', 'password2'),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', )
    ordering = ('email', 'first_name', 'last_name', 'is_admin')
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['subject', 'title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'text']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_right']
    

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'last_name', 'subject', 'test', 'total_result']
    ordering = ('user_id', 'subject', 'test')
    

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['quiz_subject', 'test']        
    