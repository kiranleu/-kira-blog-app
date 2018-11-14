from django import forms
from .models import Post

class PostForm(forms.ModelForm): #For the add Btn
    class Meta:
        model= Post
        exclude=[ 'author', 'views']
        fields ='__all__'
        
