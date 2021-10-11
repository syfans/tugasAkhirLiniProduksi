from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm

class UseRegisterForm (UserCreationForm):
    email = forms.EmailField()
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'group',
        ]