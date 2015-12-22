from django import forms
from django.contrib.auth.models import User

class login_form(forms.Form):
    login = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

class signup_form(forms.Form):  
    login_user = forms.CharField(
        label='Логин', 
        max_length=100,
        error_messages={'required': 'Пожалуйста, заполните это поле'}
        )
    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(),
        error_messages={'required': 'Пожалуйста, заполните это поле'}
        )
    again_password = forms.CharField(
        label='Еще раз пароль', 
        widget=forms.PasswordInput(),
        error_messages={'required': 'Пожалуйста, заполните это поле'}
        )
    email = forms.EmailField(
        label='Email',
        error_messages={'required': 'Пожалуйста, заполните это поле'}
        )
    
    def clean(self):
        # Определяем правило валидации
        if self.cleaned_data.get('password') != self.cleaned_data.get('again_password'):
            # Выбрасываем ошибку, если пароли не совпали
            raise forms.ValidationError('Пароли должны совпадать!')
        if User.objects.filter(username = self.cleaned_data.get('login_user')):
            raise forms.ValidationError('Логин занят!')
        return self.cleaned_data

class settings_form(forms.Form):  
    login_user = forms.CharField(
        label='Логин', 
        max_length=100,
        required = False
        )
    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(),
        required = False
        )
    again_password = forms.CharField(
        label='Еще раз пароль', 
        widget=forms.PasswordInput(),
        required = False
        )
    email = forms.EmailField(
        label='Email',
        required = False
        )
    
    avatar = forms.ImageField(
        label='Аватар',
        required = False
        )

    def clean(self):
        if self.cleaned_data.get('password'):
            if self.cleaned_data.get('password') != self.cleaned_data.get('again_password'):
                raise forms.ValidationError('Пароли должны совпадать!')
        return self.cleaned_data
class create_ask_form(forms.Form):
    title = forms.CharField(
        label='Заголовок', 
        max_length=100,
        error_messages={'required': 'Пожалуйста, заполните это поле'}
        )
    text = forms.CharField(
        label='Текст вопроса', 
        widget=forms.Textarea(),
        error_messages={'required': 'Пожалуйста, заполните это поле'}
        ) 
    tags = forms.CharField(
        label='Тэги', 
        max_length=100,
        error_messages={'required': 'Пожалуйста, заполните это поле'}
        )
