from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .validators import validate_iranian_phone
from .models import MyUser

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['phone_number', 'full_name']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd ['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("passwords dont match")
        return cd['password2']

    def save(self, commit:True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text = "you can change password using this<a href='../password/'> form</a>")

    class Meta:
        model = MyUser
        fields = ['phone_number', 'full_name', 'password', 'last_login']


class UserRegisterForm(forms.Form):
    full_name= forms.CharField(label=_('full name'),max_length=100, required=True)
    phone = forms.CharField(label=_('phone number'),max_length=11, required=True,validators=[validate_iranian_phone])
    password1 = forms.CharField(label=_('password'),widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('confirm password'),widget=forms.PasswordInput)


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = MyUser.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError(_('This phone number already exists'))
        return phone
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd ['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError(_("passwords dont match"))
        return cd['password2']


class VerifyCodeForm(forms.Form):
    code =forms.IntegerField()




class ForgotPasswordForm(forms.Form):
    phone_number = forms.CharField(label=_('phone number'),max_length=11, required=True,validators=[validate_iranian_phone])


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label=_("new password"))
    new_password2 = forms.CharField(widget=forms.PasswordInput, label=_("confirm new password"))

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(_("The passwords must be the same."))