from django import forms
from .models import ToDoListObject, Category, Point
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoListObject
        fields = ['title','category']
        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control"}),
            'category': forms.Select(attrs={"class":"form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control"})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['title']
        error_messages = None
        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        return title