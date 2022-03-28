import re
from .models import ErrorTemplate, ErrorType

def trace_hierarchy(trace):
    tracelines = trace.split("\n")
    lines = []

    for line in tracelines:
        if line == '':
            continue
        # HEAD => Header i.e. Traceback Line
        if re.search(re.escape('Traceback (most recent call last):'), line):
            lines.append([line, 'HEAD'])
        # FSUM => FrameSUMmary i.e. location info
        elif re.search('File "(.+)", line (\d+), in (.+)', line):
            res = re.search('File "(.+)", line (\d+), in (.+)', line)
            lines.append([line, 'FSUM', [res.group(1), res.group(2), res.group(3)]])
        elif re.search('File "(.+)", line (\d+)', line):
            res = re.search('File "(.+)", line (\d+)', line)
            lines.append([line, 'FSUM', [res.group(1), res.group(2), False]])
        # EXC => EXCeption i.e. template line
        # Valid ErrorType, template found
        elif match_template(line)[0].template != "Error not found":
            lines.append([line, 'EXC'])
        # Valid Template, no template found
        elif len(line.split()[0]) > 1 and len(ErrorType.objects.filter(name=line.split()[0][:-1])) > 0:
            lines.append([line, 'EXC'])
        # CARAT -> pointing ^ symbol used in SyntaxError
        elif line.strip() == "^":
            lines.append([line, 'CARAT'])
        # FSL = FrameSummaryLine i.e. the code excerpt
        # Shell form, preceded with >>>
        elif len(line) > 3 and line[0:3] == ">>>":
            lines.append([line[3:], 'FSL'])
        # Remaining is FSL without the >>>
        else:
            lines.append([line, 'FSL'])
    return lines

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
    # no template found
    unknown_trace = ErrorTemplate.objects.filter(template="Error not found").first()
    return unknown_trace, []
