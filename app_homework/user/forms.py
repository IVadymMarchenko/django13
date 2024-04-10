from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import CharField, TextInput, EmailInput, EmailField, PasswordInput
from django import forms
from quotes.models import Author, Quote, Tag
class RegisterForm(UserCreationForm):

    username=CharField(max_length=20,min_length=3,required=True,
                       widget=TextInput(attrs={'class':'form-control'}))
    email = CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = CharField(max_length=20, min_length=4, required=True,
                         widget=PasswordInput(attrs={'class': 'form-control'}))
    password2  = CharField(max_length=20, min_length=4, required=True,
                         widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields=['username', 'email','password1','password2']

class LoginForm(AuthenticationForm):
    username = CharField(max_length=20, min_length=3, required=True,
                         widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(max_length=20, min_length=4, required=True,
                          widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model=User
        fields=['username','password']


class AddAuthor(forms.ModelForm):
    fullname=CharField(required=False,max_length=50,widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))
    born_date=CharField(required=False,max_length=20,widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))
    born_location=CharField(required=False,widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))
    description=CharField(required=False,widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))

    class Meta:
        model=Author
        fields=['fullname','born_date','born_location','description']


class AddQuote(forms.ModelForm):
    tags = CharField(widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1"}))
    quote=CharField(widget=TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1", "style": "height: 200px;"}))


    class Meta:
        model=Quote
        fields = ['quote', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        return tags.split()


