from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<html><body><form action=\"/action_page.php\"><textarea name=\"message\" rows=\"10\" cols=\"30\">The cat was playing in the garden.</textarea><br><br><input type=\"submit\"></form></\body></html>")
