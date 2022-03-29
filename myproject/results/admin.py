from django.contrib import admin
from .models import ErrorTemplate, ErrorType, Example, Tip

# Register your models here.
admin.site.register(ErrorTemplate)
admin.site.register(ErrorType)
admin.site.register(Example)
admin.site.register(Tip)
