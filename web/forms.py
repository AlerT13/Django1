from django import forms
from django.contrib.auth import get_user_model

from web.models import News

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField()

    def clean(self):
        cleanes_data = super().clean()
        if cleanes_data['password'] !=cleanes_data['password2']:
            self.add_error('password', 'Пароли не совпадают')
        return cleanes_data

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class NewsForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = News
        fields = ('title', 'tags', 'text')