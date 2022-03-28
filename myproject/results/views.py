from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ErrorTemplate, ErrorType
from results.forms import SubmitErrorForm
from .tips import tip_list
import re, os
from nltk.tokenize import wordpunct_tokenize

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

    no_punct = re.sub(r'[^\w\s]','',error_trace)
    error_trace_list = no_punct.split()
    error_type_list = []
    for e in ErrorType.objects.all():
        error_type_list.append(e)
    main_error = list(set(error_trace_list).intersection(set([er.name for er in error_type_list])))
    for i in set(error_trace_list):
        if len(ErrorType.objects.filter(name=i)) > 0:
            main_error=ErrorType.objects.filter(name=i)

    # returns data into context
    num_templates = ErrorTemplate.objects.all().count()
    num_types = ErrorType.objects.all().count()

    if len(main_error) == 0:
        main_error = ErrorType.objects.filter(name="Unknown")

    main_error = main_error[0]
    result = match_template(error_trace)

    if result[1]:
        params = result[1]
    else:
        params = []
    temp = result[0]

    tags = list(temp.tags.names())
    tags.extend([p.lower() for p in params])
    relevant_tips = [tip for tip in tip_list if not set(tags).isdisjoint(tip['tags'])]
    tip_count = len(relevant_tips)

    # extract examples from examples.py based on tags
    examples = []
    for tag in tags:
        example = extract_example(tag)
        if example:
            examples.append(example)
    example_count = len(examples)

    lines = trace_hierarchy(error_trace)
    line_nums = [0]
    print(f"Lines: {lines}")

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

    lines_zipped = zip(lines, line_nums)

    indicator_count = 2
    if fsl_count > 0:
        indicator_count += 1
    if example_count > 0:
        indicator_count += 1
    if tip_count > 0:
        indicator_count += 1

    context = {
        'num_templates': num_templates,
        'num_types': num_types,
        'error_trace': error_trace,
        'error_type': main_error,
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
        'indicator_count' : indicator_count
    }
    return render(request, 'results.html', context=context)

def match_template(error_trace):
    """Method to find a error trace from the user input"""
    templates = ErrorTemplate.objects.all()
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

            # return list of single item if single item
            elif isinstance(trace_slices[0], str):
                return e, [trace_slices[0]]

            # need index 0 as trace_slices = [(param1, param2)]
            return e, trace_slices[0]
        else:
            pass#print("Search didn't work")
    unknown_trace = ErrorTemplate.objects.filter(template="Error not found").first()
    return unknown_trace, []

def trace_hierarchy(trace):
    tracelines = trace.split("\n")
    lines = []
    # print(f"tracelines: {tracelines}")
    for line in tracelines:
        if re.search(re.escape('Traceback (most recent call last):'), line):
            lines.append([line, 'HEAD'])
            # print("HEAD") # HEAD => Header i.e. Traceback Line
        elif re.search(' File "(.+)", line (\d+), in (.+)', line):
            res = re.search(' File "(.+)", line (\d+), in (.+)', line)
            lines.append([line, 'FSUM', [res.group(1), res.group(2), res.group(3)]])
        elif re.search('File "(.+)", line (\d+)', line):
            res = re.search('File "(.+)", line (\d+)', line)
            lines.append([line, 'FSUM', [res.group(1), res.group(2), False]])
            # print("FSUM") # FSUM => FrameSUMmary i.e. location info
        elif match_template(line)[0].template != "Error not found":
            lines.append([line, 'EXC'])
            # print("EXC") # EXC => EXCeption i.e. template line
        elif line.strip() == "^":
            lines.append([line, 'CARAT'])
        else:
            # print(f"line.split(): {line.split()}")
            if len(line.split()[0]) > 1 and len(ErrorType.objects.filter(name=line.split()[0][:-1])) > 0:
                lines.append([line, 'EXC'])
                # print("EXC 2") # see EXC
            elif len(line) > 3 and line[0:3] == ">>>":
                lines.append([line[3:], 'FSL'])
            else:
                lines.append([line, 'FSL'])
                # print("FSL") # FSL = FrameSummaryLine i.e. the code excerpt
    return lines

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
        print(f"Token Data: {token_data}")
        if not in_str and token == '"': # nltk token for start of string
            # print("String Entered")
            in_str = "double"
            new_str = ""
        elif not in_str and token == "'":
            in_str = "single"
            new_str = ""
        elif in_str == "double" and token == '"':
            # print("String Exited")
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

            # if len(token_data) > 1 and token_data[-2][0] == "expression":
            #     func_name = token_data[-2][1]
            #     args = token_data[-1][1][1]
            #     # remove params that are commas parsed wrong
            #     args = list(filter(lambda a: a != ["expression", ','], args))
            #     del token_data[-2:]
            #     token_data.append(["function", {"name" : func_name, "params" : args}])
            #     func_name = ""
            #     args = []
            #
            # elif len(token_data) > 1 and token_data[-2][0] == "attribute":
            #     meth_name = token_data[-2][1]
            #     args = token_data[-1][1][1]
            #     # remove params that are commas parsed wrong
            #     args = list(filter(lambda a: a != ["expression", ','], args))
            #     del token_data[-2:]
            #     token_data.append(["method", {"name" : meth_name, "params" : args}])
            #     meth_name = ""
            #     args = []
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
