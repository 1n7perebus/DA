from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField


class DreamForm(forms.ModelForm):
    MBTI_CHOICES = [
        ('', ''),
        ('INTJ', 'INTJ'),
        ('INTP', 'INTP'),
        ('ENTJ', 'ENTJ'),
        ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'),
        ('INFP', 'INFP'),
        ('ENFJ', 'ENFJ'),
        ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'),
        ('ISFJ', 'ISFJ'),
        ('ESTJ', 'ESTJ'),
        ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'),
        ('ISFP', 'ISFP'),
        ('ESTP', 'ESTP'),
        ('ESFP', 'ESFP'),
    ]

    email = forms.EmailField(required=True, label="Email")
    name = forms.CharField(required=True, label="Name")
    phone = PhoneNumberField(required=False, label="Phone Number")
    title = forms.CharField(required=True, label="Title")
    dream = forms.CharField(required=True)
    active = forms.BooleanField(required=False)
    mbti_type = forms.ChoiceField(choices=MBTI_CHOICES, label="MBTI Type")


    class Meta:
        model = Dreams
        fields = ['email', 'name', 'phone', 'title', 'dream', 'active', 'mbti_type']


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(required= True, label="Reply")
    class Meta:
        model = Reply
        fields = ['reply']


