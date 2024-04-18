import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from project.models import UserProfile
from django.core.validators import RegexValidator, FileExtensionValidator

def validate_egyptian_mobile_number(value):
    """
    Validator function to validate Egyptian mobile numbers.
    """
    if not re.match(r'^01[0-2]{1}[0-9]{8}$', value):
        raise ValidationError('Please enter a valid Egyptian mobile number.')

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserProfileRegistrationForm(forms.ModelForm):
    mobile_phone = forms.CharField(max_length=15, validators=[validate_egyptian_mobile_number])
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['mobile_phone', 'profile_picture']





egyptian_phone_validator = RegexValidator(
    regex=r'^01[0-9]{9}$',
    message='Please enter a valid Egyptian mobile phone number.'
)


class UserProfileForm(forms.ModelForm):
    mobile_phone = forms.CharField(max_length=11, validators=[egyptian_phone_validator])
   
    class Meta:
        model = UserProfile
        fields = ['mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name
    