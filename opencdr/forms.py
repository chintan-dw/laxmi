from .models import *
from django.forms import ModelForm
from django import forms

class UploadCdrForm(ModelForm):
    class Meta:
        model = UploadFile
        fields = '__all__'


class ClickForm(ModelForm):
    class Meta:
        model = UploadFile
        fields = '__all__'