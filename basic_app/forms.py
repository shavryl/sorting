from django import forms
from django.contrib.auth import password_validation
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

    class Meta():
        model = MyVeroKey
        fields = ('verokey',)



class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user



