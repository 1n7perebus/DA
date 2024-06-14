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
    #phone = PhoneNumberField(required=False, label="Phone Number")
    title = forms.CharField(required=True, label="Title")
    dream = forms.CharField(required=True)
    active = forms.BooleanField(required=False)
    mbti_type = forms.ChoiceField(choices=MBTI_CHOICES, label="MBTI Type")
    scale = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 8)], 
        label="Dream Scale", 
        initial=4, 
        widget=forms.RadioSelect
    )


    class Meta:
        model = Dreams
        fields = ['email', 'name', 'title', 'dream', 'active', 'mbti_type','scale']


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(required= True, label="Reply")
    class Meta:
        model = Reply
        fields = ['reply']


class ShareForm(forms.ModelForm):
    user = forms.CharField(required=True, label="Name")
    title = forms.CharField(required=True, label="Title")
    dream = forms.CharField(required=True)

    class Meta:
        model = Share
        fields = ['user', 'title', 'dream']