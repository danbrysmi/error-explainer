from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def error_guide(error_name):
    html = "<div>"
    html = "It looks like you got a " + error_name + "."
    html += "</div>"
    return html

def error_result(request):
    html = "<html><body>"
    html += error_guide("IndexError")
    html += "</body></html>"
    return HttpResponse(html)

def index(request):
    return HttpResponse("<html><body><form action=\"/action_page.php\"><textarea name=\"message\" rows=\"10\" cols=\"30\">The cat was playing in the garden.</textarea><br><br><input type=\"submit\"></form></\body></html>")
