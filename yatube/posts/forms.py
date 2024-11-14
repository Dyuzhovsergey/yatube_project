from django import forms
from .models import Post, Comment

#  создадим собственный класс для формы создания записи
#  сделаем его наследником предустановленного класса ModelForm
class PostForm(forms.ModelForm):
    class Meta():
        # укажем модель, с которой связана создаваемая форма
        model = Post
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('text', 'group', 'image')
        
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст', 'style': 'border: 2px solid #ccc;'}),
            'group': forms.Select(attrs={'class': 'form-control', 'style': 'border: 2px solid #ccc; padding: 15px;'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'style': 'border: 2px solid #ccc; padding: 15px;', 'title': 'Загрузите ваше изображение здесь'}),
        }  
        
class CommentForm(forms.ModelForm):
    class Meta():
        # укажем модель, с которой связана создаваемая форма
        model = Comment
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('text',)

