# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserWords

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class FileUploadForm(forms.Form):
    file = forms.FileField(required= True,label='Select a file',widget=forms.FileInput(attrs={'accept': '.docx,.pdf,.txt'}))


class EditWordForm(forms.ModelForm):
    class Meta:
        model = UserWords
        fields = ('word', 'translation')
        labels = {
            'word': 'Word',
            'translation': 'Translation',
        }