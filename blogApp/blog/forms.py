from django import forms
from .models import Post


class UploadForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'post_image']