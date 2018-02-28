from django import forms

from hangout.models import Hangout


class HangoutForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    address = forms.CharField(required=True)

    class Meta:
        model = Hangout
        fields = ['title', 'description', 'address']
