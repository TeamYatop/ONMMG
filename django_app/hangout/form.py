from django import forms

from hangout.models import Hangout, Area, Tag


class HangoutForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    address = forms.CharField(required=True)

    class Meta:
        model = Hangout
        fields = ['title', 'description', 'address']


class AreaForm(forms.ModelForm):
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)

    class Meta:
        model = Area
        fields = ['name', 'address']


class TagForm(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=Area.objects.all(), empty_label="(Nothing)", required=False)

    class Meta:
        model = Tag
        fields = ['area']
