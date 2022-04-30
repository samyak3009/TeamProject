from secrets import choice
from django import forms
from .models import Post,Category



choice_list=Category.objects.all().values_list('name', 'name').order_by()
class UploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_image', 'category']
        widgets={
            'category': forms.Select(choices=choice_list,attrs={'class':'form-control'})
        }
    def __init__(self,*args,**kwargs):
        # print(self)
        super(UploadForm, self).__init__(*args, **kwargs)
        # self.fields['category'].choices = []
        print(self)
        try :
            choice=Category.objects.all().values_list('id', 'name').order_by()
            self.fields['category'].choices = choice
        except(ValueError, TypeError):
            pass
        print(self.fields['category'].choices,"sasasa")




