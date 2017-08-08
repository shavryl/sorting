from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, MyVeroKey




class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'lastname', 'city', 'country', 'phonenumber', 'email', 'date_of_birth')


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(help_text=False)

    class Meta():
        model = User
        fields = ('username','password')



class VeroKeyForm(ModelForm):
    verokey = forms.CharField(label="vero_key", help_text='input your GetVero key here, please')
    id = forms.IntegerField(required=False)

    class Meta():
        model = MyVeroKey
        fields = ('verokey',)



class UserPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('password mismatch')





