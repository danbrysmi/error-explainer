from django.contrib import admin
from .models import ErrorTemplate, ErrorType

# Register your models here.
admin.site.register(ErrorTemplate)
admin.site.register(ErrorType)
