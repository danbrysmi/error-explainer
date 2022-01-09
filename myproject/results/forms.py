from django import forms

class SubmitErrorForm(forms.Form):
    error_trace = forms.CharField(widget=forms.Textarea)
