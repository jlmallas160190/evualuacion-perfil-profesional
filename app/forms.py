#encoding:utf-8 
from django.forms import ModelForm
from django import forms
from app.models import Test
class TestForm(ModelForm):
    class Meta:
        model = Test