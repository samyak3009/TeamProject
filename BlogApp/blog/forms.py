from secrets import choice
from django import forms
from .models import Post,Category


choice_list=[]

class UploadForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'post_image', 'category']
        widgets={
            'category': forms.Select(choices=choice_list,attrs={'class':'form-control'})
        }
    def __init__(self,*args,**kwargs):
        print("samayk")
        super(UploadForm, self).__init__(*args, **kwargs)
        choice = []
        choices_list=Category.objects.all().values_list('name', 'name')        
        for item in choices_list:
            choice.append(item)
        print(self.fields['category'].choices)
        self.fields['category'].choices = choice




