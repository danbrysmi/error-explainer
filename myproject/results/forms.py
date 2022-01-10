from django import forms

placeholder_error = "Try pasting your error in here:\n\nTraceback (most recent call last):\n  File \"<mypythonfile>\", line 1, in <module>\n    print(\"Hello World\")\nAnnoyingError: cannot understand your amazing python :("
class SubmitErrorForm(forms.Form):
    error_trace = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 400, 'placeholder': placeholder_error}))
