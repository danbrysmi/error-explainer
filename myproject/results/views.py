from django.shortcuts import render
from django.http import HttpResponse
from .models import ErrorTemplate, ErrorType
from results.forms import SubmitErrorForm
import re

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
    """View function for home page of site."""
    form = None
    # Generate counts of some of the main objects
    # all is implied by default
    num_templates = ErrorTemplate.objects.all().count()
    num_types = ErrorType.objects.all().count()

    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    if request.method == "GET":
        proposed_error_type = "help :("
        form = SubmitErrorForm(initial={'error_trace': proposed_error_type})

    context = {
        'num_templates': num_templates,
        'num_types': num_types,
        'form': form
    }
    return render(request, 'index.html', context=context)

def solve(request):
    """View function for presenting answers to the error trace."""
    error_trace = request.GET['error_trace']
    # NLTK CODE GOES HERE
    no_punct = re.sub(r'[^\w\s]','',error_trace)
    error_trace_list = no_punct.split()
    error_type_list = []
    for e in ErrorType.objects.all():
        error_type_list.append(e.name)
    #print(error_type_list)
    main_error = list(set(error_trace_list).intersection(error_type_list))
    print(main_error)
    # returns data into context
    num_templates = ErrorTemplate.objects.all().count()
    num_types = ErrorType.objects.all().count()

    context = {
        'num_templates': num_templates,
        'num_types': num_types,
        'error_trace': error_trace,
        'error_type': main_error[0],
    }
    return render(request, 'results.html', context=context)
