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
