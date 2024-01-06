from django import forms
from home.models import *

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file']

