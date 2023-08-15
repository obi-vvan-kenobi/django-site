from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError

from .models import *
from betterforms.multiform import MultiModelForm
import sys

# sys.path.append("..")

from utils.send_mail import send_email


class TurnOffSave:
    def save(self, commit=True):
        return


class ContactForm(TurnOffSave, forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        user_email = cleaned_data.get('email')
        form_user_name = cleaned_data.get('name')
        if not User.objects.filter(email=user_email).exists():
            raise ValidationError(
                'Пользователя с таким email не существует!'
            )
        user = Contact.objects.filter(email=user_email)
        if user:
            user_name = user.values('name')[0]['name']
            if user_name != form_user_name:
                raise ValidationError(
                    f'Пользователь с таким email указывал другое имя: {user_name}!'
                )


class ContactFormMessage(TurnOffSave, forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = ContactMessages
        fields = ('message',)


class ContactMultiForm(MultiModelForm):
    form_classes = {
        'contact': ContactForm,
        'contact_message': ContactFormMessage,
    }

    def save(self, commit=True):
        contact = self.cleaned_data['contact']
        contact, created = Contact.objects.get_or_create(name=contact['name'], email=contact['email'],
                                                         telephone_number=contact['telephone_number'])
        message = self.cleaned_data['contact_message']['message']
        ContactMessages(contact_id=contact.pk, message=message).save()
        send_email(message, contact['email'])
        return super().save(commit=True)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
