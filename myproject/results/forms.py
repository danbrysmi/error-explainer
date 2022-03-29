from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from .utils import trace_hierarchy

placeholder_error = "Try pasting your error in here:\n\nTraceback (most recent call last):\n  File \"<mypythonfile>\", line 1, in <module>\n    print(\"Hello World\")\nAnnoyingError: cannot understand your amazing python :("

def validate_trace(value):
    lines = trace_hierarchy(value)
    exc_count = 0
    for line_id in range(len(lines)):
        if lines[line_id][1] == 'EXC':
            exc_count += 1
    print(f'EXC COUNT: {exc_count}')
    if exc_count == 0:
        raise ValidationError("You need to include your error!")
    elif exc_count > 1:
        raise ValidationError("Only put in one error at a time please!")

class SubmitErrorForm(forms.Form):
    error_trace = forms.CharField(
    label='',
    validators=[validate_trace],
    widget=forms.Textarea(attrs={'rows': 16, 'cols': 400, 'placeholder': placeholder_error, 'style': 'font-family: inconsolata'})
     )
