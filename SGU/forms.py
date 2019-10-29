from django import forms
from django.forms import ModelForm
from SGU.models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _

class form_usuario(ModelForm):
    password = forms.CharField(label='senha', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput())
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    class Meta():
        model = Usuario
        fields = ['username', 'nome', 'email', 'password', 'password2']
    
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(form_usuario, self).save(commit=False)
        user.tipo = 'E'
        user.set_password(user.password)
        if commit:
            user.save()
        return user

class form_cliente(ModelForm):
    password = forms.CharField(label='senha', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar senhar',widget=forms.PasswordInput())
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    class Meta():
        model = Usuario
        fields = ['nome', 'email', 'password', 'password2', 'cpf', 'cep']

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    def save(self, commit=True):
        user = super(form_cliente, self).save(commit=False)
        user.username = self.cleaned_data.get("email")
        user.tipo = 'C'
        user.set_password(user.password)
        if commit:
            user.save()
        return user
        
class LoginForm(forms.Form):
    username = forms.CharField(label=(u'Username'))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))