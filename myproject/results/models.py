from django.db import models
import uuid
from django.forms import ModelForm, Textarea
from taggit.managers import TaggableManager
# Create your models here.
class ErrorType(models.Model):
    """Model representing a python traceback error type."""
    name = models.CharField(max_length=30, help_text="Must be a python error class, e.g. TypeError")
    desc = models.TextField(max_length=400, help_text="A brief description of the type of error (using markdown)")
    def __str__(self):
        """String for representing the Model object."""
        return f"Name: {self.name} \nDesc: {self.desc}"

class ErrorTemplate(models.Model):
    """Model representing a python traceback error template."""
    template = models.CharField(max_length=400, help_text='The template to be matched, using <n> for wildcards starting with <1>.')
    error_type = models.ForeignKey('ErrorType', on_delete=models.SET_NULL, null=True, help_text='The type of error, e.g. TypeError')
    short_desc = models.TextField(max_length=800, help_text="A brief description of the specific trace (using markdown)")
    tags = TaggableManager()

    def __str__(self):
        """String for representing the Model object."""
        return self.template

class Example(models.Model):
    """Model representing code that is a worked example of an error, called in the Worked Examples slide."""
    code_wrong = models.TextField(max_length=800, help_text='Incorrect code example.')
    code_right = models.TextField(max_length=800, help_text='Correct code example.')
    desc_wrong = models.TextField(blank=True, max_length=800, help_text='Why does the incorrect code not work?')
    desc_right = models.TextField(blank=True, max_length=800, help_text='Why does the correct code work?')
    tags = TaggableManager()

    def __str__(self):
        """String for representing the Model object."""
        return " ".join(o for o in self.tags.names()) + " | " + self.code_wrong

class Tip(models.Model):
    """Model representing a tip that is called in the Further Resources slide."""
    name = models.CharField(max_length=50, help_text='Title of tip')
    desc = models.TextField(max_length=800, help_text='Tip main text')
    link = models.URLField(max_length=400, help_text='Link to resource')
    tags = TaggableManager()

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name} | {self.desc}"
