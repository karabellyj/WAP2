from django import forms
from .models import File
from .widgets import BootstrapDateTimePickerInput

class UpdateExpiryFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('expire_at',)
        widgets = {
            'expire_at': BootstrapDateTimePickerInput(attrs={
                'readonly': ''
            })
        }


class CreateFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', 'expire_at')
        widgets = {
            'expire_at': BootstrapDateTimePickerInput(attrs={
                'readonly': ''
            })
        }