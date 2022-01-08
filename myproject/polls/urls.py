from django.urls import path

from . import views

# path(route, view, kwargs, name)
# params:
#   route - string that contains a URL urlpattern
#   view - specified view function (has a HTTPRequest as the first argument, captured values as keyword args)
#   kwargs - arbitary keyword arguments can be passed in a dictionary (? tbd)
#   name - naming your URL so it can be referred to from elsewhere in Django
urlpatterns = [
    path('', views.index, name='index'),
]
