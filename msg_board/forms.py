from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Post, Comment, Category


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана",
                                      label="Категории")
    content = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = Post
        fields = ['heading', 'content', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
            'confirm',
        ]
