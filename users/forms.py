from django import forms
from django.contrib.auth.models import User
from users.models import Profile

class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        labels = {
            'username':'Ulanyjy Ady',
            'email':'Elektron Poşta',
        }


class profileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['bio','profile_pic']
        labels = {
            'bio':'Özün Barada',
            'profile_pic':'Profil Suraty',
        }
