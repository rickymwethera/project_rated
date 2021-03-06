from django import forms
from django.contrib.auth.models import User
from .models import Project, Profile, Rate

class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('id','image','title','link','description')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('id','profile_picture','bio') 

class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('design','usability','content')