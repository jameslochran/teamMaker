from django import forms

class RosterForm(forms.Form):
    available = forms.BooleanField(required=False)
