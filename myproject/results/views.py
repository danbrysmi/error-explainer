from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ErrorTemplate, ErrorType
from results.forms import SubmitErrorForm
from .tips import tip_list
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
        proposed_error_type = ""
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
    #print(main_error)
    # returns data into context
    num_templates = ErrorTemplate.objects.all().count()
    num_types = ErrorType.objects.all().count()

    if len(main_error) == 0:
        main_error = ErrorType.objects.filter(name="Unknown")
    main_error = main_error[0]
    print(main_error)
    result = match_template(error_trace, main_error)

    params = result[1]
    temp = result[0]

    print(result)
    print(params)
    tags = list(temp.tags.names())
    tags.extend(params)
    relevant_tips = [tip for tip in tip_list if not set(tags).isdisjoint(tip['tags'])]

    context = {
        'num_templates': num_templates,
        'num_types': num_types,
        'error_trace': error_trace,
        'error_type': main_error,
        'error_template': temp,
        'params': params,
        'tags' : tags,
        'tips' : relevant_tips
    }
    return render(request, 'results.html', context=context)

def match_template(error_trace, etype):
    """Method to find a error trace from the user input"""
    e_type = get_object_or_404(ErrorType, name=etype)
    templates = ErrorTemplate.objects.all().filter(error_type = e_type)
    print(f"{len(templates)} templates found")
    for e in templates:
        # make sure regex characters are escaped before replacing
        pattern_str = re.escape(e.template)
        # replace <n> with wildcard
        pattern_str = re.sub("<.*?>", "'(.*?)'", pattern_str)

        # match wildcards to params
        if re.search(pattern_str, error_trace):
            trace_slices = re.findall(pattern_str, error_trace)
            # return empty params if no wildcard matching
            if trace_slices == []:
                return e, []
            # need index 0 as trace_slices = [(param1, param2)]
            return e, trace_slices[0]
        else:
            print("Search didn't work")
    unknown_trace = ErrorTemplate.objects.filter(template="Error not found").first()
    return unknown_trace, []
