from django import forms
from .models import Profile, TestsFolder

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture' , 'name','surname', 'gpa' ]
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your bio...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'GPA (e.g. 3.75)'})
        }

class FolderForm(forms.ModelForm):
    class Meta:
        model = TestsFolder
        fields = ['folder_name']
