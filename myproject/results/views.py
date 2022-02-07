from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ErrorTemplate, ErrorType
from results.forms import SubmitErrorForm
from .tips import tip_list
import re, os

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

    if result[1]:
        params = result[1]
    else:
        params = []
    temp = result[0]

    #print(result)
    #print(params)
    tags = list(temp.tags.names())
    tags.extend([p.lower() for p in params])
    relevant_tips = [tip for tip in tip_list if not set(tags).isdisjoint(tip['tags'])]

    # extract examples from examples.py based on tags
    examples = []
    for tag in tags:
        print(tag)
        example = extract_example(tag)
        if example:
            examples.append(example)

    #example =
    context = {
        'num_templates': num_templates,
        'num_types': num_types,
        'error_trace': error_trace,
        'error_type': main_error,
        'error_template': temp,
        'params': params,
        'tags' : tags,
        'tips' : relevant_tips,
        'examples' : examples
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
        print(pattern_str)
        # replace <n> with wildcard
        pattern_str = re.sub("<.*?>", "'(.*?)'", pattern_str)
        print(pattern_str)

        # match wildcards to params
        if re.search(pattern_str, error_trace):
            trace_slices = re.findall(pattern_str, error_trace)
            print(trace_slices)
            # return empty params if no wildcard matching
            if trace_slices == []:
                return e, []
            elif isinstance(trace_slices[0], str):
                return e, False
            # need index 0 as trace_slices = [(param1, param2)]
            return e, trace_slices[0]
        else:
            print("Search didn't work")
    unknown_trace = ErrorTemplate.objects.filter(template="Error not found").first()
    return unknown_trace, []

def extract_example(param):
    # use absolute path
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'examples.py')
    f = open(filename, 'r')
    f_list = f.readlines()

    tag_found = False
    end_tag = False
    c = 0
    #print(len(f_list))
    example_text = ""

    # gather the text from .py file from param tag to the next tag (denoted by ##)
    while not (tag_found and end_tag) and c < len(f_list):
        #print(f"{c} {f_list[c]}", end="")
        if not tag_found:
            if f_list[c] == "## " + param + "\n":
                #print("Start tag found!")
                tag_found = True

        elif not end_tag:
            if len(f_list[c]) > 1 and f_list[c][0:2] == "##":
                #print("Next tag found!")
                end_tag = True
            else:
                example_text += f_list[c]
        c += 1

    # False if tag section was not located or end tag not found
    if not tag_found or not end_tag:
        return False

    return example_text
