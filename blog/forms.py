
from django import forms
from .models import CustomUser

class CustomUserSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
       
