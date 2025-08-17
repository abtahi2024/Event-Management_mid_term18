from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from evenapp.forms import StyledFormMixin
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from users.models import CustomUser
from django.contrib.auth.models import Group,Permission

class RegisterForm(StyledFormMixin,UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','password1','password2']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldsname in self.fields:
            self.fields[fieldsname].help_text=None

class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

class AssignRoleForm(StyledFormMixin,forms.Form):
    role=forms.ModelChoiceField(queryset=Group.objects.all(),empty_label='selected Roll')


class createfrom(StyledFormMixin,forms.ModelForm):
    permissions=forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),widget=forms.CheckboxSelectMultiple,required=False,label='Assign permission')
    class Meta:
        model=Group
        fields=['name','permissions']

class CustomPasswordChangeForm(StyledFormMixin,PasswordChangeForm):
    pass

class  CustomPasswordResetForm(StyledFormMixin,PasswordResetForm):
    pass

class CustomPasswordResetConfirmForm(StyledFormMixin,SetPasswordForm):
    pass

class EditProfileForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['email','first_name','last_name','profile_image','phone']