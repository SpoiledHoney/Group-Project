from django import forms
from .models import Post

class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_image']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }