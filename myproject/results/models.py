from django.db import models
import uuid
from django.forms import ModelForm, Textarea
# Create your models here.
class ErrorTemplate(models.Model):
    """Model representing a python traceback error template."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id for this particular template.")
    template = models.CharField(max_length=400, help_text='Paste your error trace here!')
    error_type = models.ForeignKey('ErrorType', on_delete=models.SET_NULL, null=True)

    # class Meta:
    #     widgets = {
    #         'content': Textarea(attrs={'cols': 80, 'rows': 20}),
    #     }
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.error_type.name} Template ID: {self.id}"

class ErrorType(models.Model):
    """Model representing a python traceback error type."""
    name = models.CharField(max_length=30, help_text="Must be a python error class, e.g. TypeError")

    def __str__(self):
        """String for representing the Model object."""
        return self.name
