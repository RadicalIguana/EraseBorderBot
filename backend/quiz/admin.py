from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Subject, Test, Question, Answer, Quiz, MyUser, Result

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        # fields = ('email', 'date_of_birth')
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        # fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')
        fields = ('email', 'password', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    # list_display = ('email', 'date_of_birth', 'is_admin')
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'fields': ('email', 'date_of_birth', 'password1', 'password2'),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'first_name', 'last_name', 'phone')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['subject', 'test_number', 'title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'text']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_right']
    
    
# @admin.register(Result)
# class ResultAdmin(admin.ModelAdmin):
#     list_display = ['user_id', 'subject', 'test', 'result']


# class QuizAdminForm(forms.ModelForm):
#     class Meta:
#         model = Quiz
#         exclude = ['subject', 'test', 'question', 'answer']
        
#     subjects = forms.ModelChoiceField(queryset=Subject.objects.all())
#     print(subjects)
        
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['subject', 'test']
    
