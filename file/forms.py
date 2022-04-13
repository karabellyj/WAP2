from django import forms
from .models import File

class CreateFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', 'expire_at')