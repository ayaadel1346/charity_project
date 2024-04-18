from django import forms
from django.contrib.auth.models import User
from project.models import UserProfile
from django.core.validators import RegexValidator
from project.models import Category
from project.models import FeaturedProject, Project


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
        fields = ['username', 'first_name', 'last_name', 'email']

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
    

class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
            raise forms.ValidationError(
                "Password and confirm password do not match"
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AddUserProfileForm(forms.ModelForm):
    mobile_phone = forms.CharField(max_length=11, validators=[egyptian_phone_validator])
   
    class Meta:
        model = UserProfile
        fields = ['mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country']




class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  





class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']






class FeaturedProjectForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None, label='Project')
    
    class Meta:
        model = FeaturedProject
        fields = ['project', 'is_featured']
