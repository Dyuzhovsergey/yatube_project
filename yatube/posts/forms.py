from django import forms
from .models import Post

#  создадим собственный класс для формы создания записи
#  сделаем его наследником предустановленного класса ModelForm
class PostForm(forms.ModelForm):
    class Meta():
        # укажем модель, с которой связана создаваемая форма
        model = Post
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('text', 'group', )
        
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст'}),
            'group': forms.Select(attrs={'class': 'form-control', }),
        }  
        
