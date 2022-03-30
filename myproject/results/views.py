from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import ErrorTemplate, ErrorType, Example, Tip
from results.forms import SubmitErrorForm
from .utils import trace_hierarchy, match_template
import re, os
from nltk.tokenize import wordpunct_tokenize

# Create your views here.
def index(request):
    """View function for home page of site."""
    form = None
    # Generate counts of some of the main objects
    # all is implied by default
    num_templates = ErrorTemplate.objects.all().count()
    num_types = ErrorType.objects.all().count()

    # First time = empty form
    if request.method == "GET":
        form = SubmitErrorForm()

    # After form submission
    elif request.method == "POST":
        form = SubmitErrorForm(request.POST)
        if form.is_valid():
            # Store trace info in session to be used in solve()
            trace = form.cleaned_data['error_trace']
            request.session['error_trace'] = trace
            return HttpResponseRedirect(reverse('solve'))

    context = {
        'num_templates': num_templates,
        'num_types': num_types,
        'form': form
    }

    return render(request, 'index.html', context=context)

def solve(request):
    """View function for presenting answers to the error trace."""
    # get trace from session
    error_trace = request.session.get('error_trace', '')

    # remove punctation
    no_punct = re.sub(r'[^\w\s]','',error_trace)

    # returns data into context
    num_templates = ErrorTemplate.objects.all().count()
    num_types = ErrorType.objects.all().count()

    # matching trace to possible templates
    result = match_template(error_trace)

    if result[1]:
        params = result[1]
    else:
        params = []
    temp = result[0]

    # get list of applicable tags and wildcards from the <n>'s in the template
    tags = list(temp.tags.names())
    tags.extend([p.lower() for p in params])

    relevant_tips = list(Tip.objects.filter(tags__name__in=tags))

    # if tip_count = 0, no point showing tip page on carousel
    tip_count = len(relevant_tips)

    # extract examples from examples.py based on tags (change me to a model!)
    examples = []
    examples = list(Example.objects.filter(tags__name__in=tags))
        # example = extract_example(tag)
        # if example:
        #     examples.append(example)
    example_count = len(examples)

    # get trace hierarchy
    lines = trace_hierarchy(error_trace)

    # get type of error
    error_type = ""
    exc_line = [line for line in lines if line[1]=='EXC']

    if len(ErrorType.objects.filter(name=exc_line[-1][0].split()[0][:-1])) > 0:
        error_type = ErrorType.objects.filter(name=exc_line[-1][0].split()[0][:-1]).first()
    else:
        error_type = ErrorType.objects.filter(name="Unknown").first()

    # offset line numbers so FSUM line above gives FSL line number for reference
    line_nums = [0]
    print(f"Lines: {lines}")

    # if fsl_count = 0 no need to show code breakdown in carousel
    fsl_count = 0
    for line_id in range(len(lines)):
        if lines[line_id][1] == 'FSL':
            fsl_count += 1
            parsed_line = tokenise_fsl(lines[line_id][0])
            lines[line_id].append(parsed_line)
        l_num = lines[line_id][2][1] if lines[line_id][1] == 'FSUM' else 0
        line_nums.append(l_num)
    line_nums.pop(-1)
    print(f"Lines (new): {lines}")
    # zip two lists together so they can be iterated simultaneously in template
    lines_zipped = zip(lines, line_nums)

    # count of total number of items needed in carousel and last item number
    indicator_count = 2
    last_item = 3
    if fsl_count > 0:
        indicator_count += 1
    if example_count > 0:
        indicator_count += 1
        last_item = 4
    if tip_count > 0:
        indicator_count += 1
        last_item = 5
    print(f"error_type: {error_type}")
    context = {
        'num_templates': num_templates,
        'num_types': num_types,
        'error_trace': error_trace,
        'error_type': error_type,
        'error_template': temp,
        'params': params,
        'tags' : tags,
        'tips' : relevant_tips,
        'examples' : examples,
        'lines' : lines,
        'lines_zipped' : lines_zipped,
        'fsl_count' : fsl_count,
        'example_count' : example_count,
        'tip_count' : tip_count,
        'indicator_count' : indicator_count,
        'last_item' : last_item
    }
    return render(request, 'results.html', context=context)



def tokenise_fsl(fsl_line):
    print("="*100)
    tokens_raw = wordpunct_tokenize(fsl_line)

    tokens = []
    for token in tokens_raw:
        if not all(not c.isalnum() for c in token):
            tokens.append(token)
        else:
            tokens = tokens + list(token)
    print(f"Tokens (after specials): {tokens}")
    in_str = False
    new_str = ""
    in_brackets = 0
    in_square = 0
    func_name = ""
    meth_name = ""
    args = []
    token_data = []

    for token in tokens:
        if not in_str and token == '"':
            in_str = "double"
            new_str = ""
        elif not in_str and token == "'":
            in_str = "single"
            new_str = ""
        elif in_str == "double" and token == '"':
            in_str = False
            token_data.append(["string", new_str])
        elif in_str == "single" and token == "'":
            in_str = False
            token_data.append(["string", new_str])
        elif in_str:
            if len(new_str) > 0:
                new_str += " " + token
            else:
                new_str += token
        elif token in ["and", "not", "or", "+", "=", "+=", "==", ">=", "<=", ">", "<", "!=", "-", "/", "//", "%", "*", "-=", "/=", "*=", "**"]:
            token_data.append(["operator", token])
            if len(token_data) > 1 and token_data[-2][0] == "operator":
                test_token = token_data[-2][1] + token_data[-1][1]
                if test_token in ["and", "not", "or", "+", "=", "+=", "==", ">=", "<=", ">", "<", "!=", "-", "/", "//", "%", "*", "-=", "/=", "*=", "**"]:
                    del token_data[-2:]
                    token_data.append(["operator", test_token])
        # elif token in ["abs", "all", "any", "bool", "chr", "dict", "enumerate", "eval", "float", "format", "help", "hex", "id", "input", "int", "isinstance", "len", "list", "map", "max", "min", "oct", "open", "ord", "pow", "print", "range", "repr", "reversed", "round", "set", "slice", "sorted", "str", "sum", "super", "tuple", "type"]:
        #     token_data.append(["built-in function", token])
        elif token in ["if", "elif", "else", "while", "for", "break", "continue", "return", "match"]:
            token_data.append(["control", token])
        elif token.isnumeric():
            if len(token_data) > 1 and token_data[-1] == ["expression", "."] and token_data[-2][0] == "int":
                n = token_data.pop(-2)
                token_data.pop(-1)
                token_data.append(["float", n[1] + "." + token])
            elif len(token_data) > 0 and token_data[-1] == ["expression", "."]:
                token_data.pop(-1)
                token_data.append(["float", "0." + token])
            else:
                token_data.append(["int", token])
        elif token == "(":
            in_brackets += 1
            token_data.append(["bracket_start", "("])
        elif token == "[":
            in_square += 1
            token_data.append(["square_start", "["])
        elif token == ")" and in_brackets:
            in_brackets -= 1
            token_data.append(["bracket_end", ")"])
            #lbi = last bracket index
            lbi = len(token_data) - 1 - token_data[::-1].index(["bracket_start", "("])
            token_data.append(["brackets", ["items", token_data[lbi+1:-1]]])
            del token_data[lbi:-1]

            if len(token_data) > 1 and token_data[-2][0] == "expression":
                func_name = token_data[-2][1]
                args = token_data[-1][1][1]
                # remove params that are commas parsed wrong
                args = list(filter(lambda a: a != ["expression", ','], args))
                del token_data[-2:]
                token_data.append(["function", {"name" : func_name, "params" : args}])
                func_name = ""
                args = []

            elif len(token_data) > 1 and token_data[-2][0] == "attribute":
                meth_name = token_data[-2][1]
                args = token_data[-1][1][1]
                # remove params that are commas parsed wrong
                args = list(filter(lambda a: a != ["expression", ','], args))
                del token_data[-2:]
                token_data.append(["method", {"name" : meth_name, "params" : args}])
                meth_name = ""
                args = []
        elif token == "]" and in_square:
            in_square -= 1
            token_data.append(["square_end", ")"])
            #lbi = last bracket index
            lbi = len(token_data) - 1 - token_data[::-1].index(["square_start", "["])
            token_data.append(["square_brackets", ["items", token_data[lbi+1:-1]]])
            del token_data[lbi:-1]
        elif token == ":":
            token_data.append(["colon", token])
        elif token == ",":
            token_data.append(["comma", ','])
        else:
            if len(token_data) > 0 and token_data[-1] == ["expression", "."]:
                token_data.remove(["expression", "."])
                token_data.append(["attribute", token])
            else:
                token_data.append(["expression", token])
    else:
        if in_str: # unclosed string
            token_data.append(["string-semi", '"' + new_str])

    print(f"Token Data: {token_data}")
    print("="*100)

    return token_data
