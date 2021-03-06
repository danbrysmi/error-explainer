from django.test import TestCase
from results.models import ErrorTemplate, ErrorType
from results.views import tokenise_fsl
from results.utils import match_template, trace_hierarchy
# Create your tests here.

#################
# MODEL TESTING #
#################
# class ErrorTemplateTestCase(TestCase):
#
#
#     def test_filter_by_error(self):
#         """Errors are correctly filtered by type."""
#         new_errors = ErrorTemplate.objects.filter(error_type=self.e_type)
#         self.assertEqual(len(new_errors), 1)

#################
# VIEW TESTING #
#################

# Template Matching
class MatchTemplateTestCase(TestCase):
    def setUp(self):
        self.e_type = ErrorType.objects.create(name="NewError")
        self.unk_e_type = ErrorType.objects.create(name="Unknown")
        ErrorTemplate.objects.create(template="Error not found", error_type = self.unk_e_type)
        ErrorTemplate.objects.create(template="NewError: <1> is wrong", error_type = self.e_type)

    def test_invalid_error(self):
        """Invalid Errors are given the Unknown Error class."""
        trace = "not sure what this error is"
        temp = match_template(trace)
        self.assertEqual(temp[0].error_type, self.unk_e_type)

    def test_param_match(self):
        trace = "NewError: 'dan' is wrong"
        temp = match_template(trace)
        self.assertEqual(temp[0].error_type, self.e_type)
        self.assertEqual(temp[0].template, "NewError: <1> is wrong")

class TraceHierarchyTestCase(TestCase):
    def setUp(self):
        self.good_test_trace = 'Traceback (most recent call last):\n  File "<pyshell#0>", line 1, in <module>\n    1 + "d"\nNewError: \'dan\' is wrong'
        self.unk_e_type = ErrorType.objects.create(name="Unknown")
        ErrorTemplate.objects.create(template="Error not found", error_type = self.unk_e_type)
        self.e_type = ErrorType.objects.create(name="NewError")
        ErrorTemplate.objects.create(template="NewError: <1> is wrong", error_type = self.e_type)

    def test_good_trace(self):
        test_lines = trace_hierarchy(self.good_test_trace)
        expected_classes = ['HEAD', 'FSUM', 'FSL', 'EXC']
        for t in range(len(test_lines)):
            self.assertEqual(test_lines[t][1], expected_classes[t])

class TokeniseFslTestCase(TestCase):

    def test_recognise_string(self):
        # single quoted
        data = tokenise_fsl("'hello'")
        self.assertEqual(data, [["string", 'hello']])

    def test_recognise_string_double(self):
        # double quoted
        data = tokenise_fsl('"hello"')
        self.assertEqual(data, [["string", "hello"]])

    def test_reconise_multiword_string(self):
        #single quoted multi
        data = tokenise_fsl("'hello world'")
        self.assertEqual(data, [["string", 'hello world']])

    def test_reconise_multiword_string_double(self):
        # double quoted multi
        data = tokenise_fsl('"hello world"')
        self.assertEqual(data, [["string", "hello world"]])

    def test_escaped_single_quote(self):
        # escaped '
        data = tokenise_fsl("'don\\'t'")
        self.assertEqual(data, [["string", "don\\'t"]])

    def test_escaped_speech(self):
        data = tokenise_fsl("'\\\"Hurry!\\\"'")
        self.assertEqual(data, [["string", '\\"Hurry!\\"']])

    def test_recognise_int(self):
        data = tokenise_fsl("3")
        self.assertEqual(data, [["int", "3"]])

    def test_recognise_float(self):
        data = tokenise_fsl("2.5")
        self.assertEqual(data, [["float", "2.5"]])

    def test_recognise_decimal(self):
        data = tokenise_fsl(".5")
        self.assertEqual(data, [["float", "0.5"]])

    def test_recognise_brackets_empty(self):
        data = tokenise_fsl("()")
        self.assertEqual(data, [["brackets", ["items", []]]])

    def test_recognise_brackets_1item(self):
        data = tokenise_fsl("(5)")
        self.assertEqual(data, [["brackets", ["items", [["int", "5"]]]]])

    def test_recognise_brackets_Nitems(self):
        data = tokenise_fsl("(5, 6)")
        self.assertEqual(data, [["brackets", ["items", [["int", "5"], ["comma", ","], ["int", "6"]]]]])

    def test_recognise_nested_brackets(self):
        data = tokenise_fsl("(1, (1, 2))")
        self.assertEqual(data, [["brackets", ["items", [["int", "1"], ["comma", ","], ["brackets", ["items", [["int", "1"], ["comma", ","], ["int", "2"]]]]]]]])

    def test_recognise_squ_brackets_empty(self):
        data = tokenise_fsl("[]")
        self.assertEqual(data, [["square_brackets", ["items", []]]])

    def test_recognise__squ_brackets_1item(self):
        data = tokenise_fsl("[5]")
        self.assertEqual(data, [["square_brackets", ["items", [["int", "5"]]]]])

    def test_recognise__squ_brackets_Nitems(self):
        data = tokenise_fsl("[5, 6]")
        self.assertEqual(data, [["square_brackets", ["items", [["int", "5"], ["comma", ","], ["int", "6"]]]]])

    def test_recognise__squ_nested_brackets(self):
        data = tokenise_fsl("[1, [1, 2]]")
        self.assertEqual(data, [["square_brackets", ["items", [["int", "1"], ["comma", ","], ["square_brackets", ["items", [["int", "1"], ["comma", ","], ["int", "2"]]]]]]]])

    def test_recognise_function(self):
        data = tokenise_fsl("my_func()")
        self.assertEqual(data, [["function", {"name" : "my_func", "params" : []}]])

    def test_recognise_function_1param(self):
        data = tokenise_fsl("my_func(arg1)")
        self.assertEqual(data, [["function", {"name" : "my_func", "params" : [["expression", "arg1"]]}]])

    def test_recognise_function_Nparam(self):
        data = tokenise_fsl("my_func(arg1, arg2, arg3)")
        self.assertEqual(data, [["function", {"name" : "my_func", "params" : [["expression", "arg1"], ["comma", ","], ["expression", "arg2"], ["comma", ","], ["expression", "arg3"]]}]])

    def test_recognise_nested_function(self):
        data = tokenise_fsl("my_func1(my_func2())")
        self.assertEqual(data, [["function", {"name" : "my_func1", "params" : [["function", {"name" : "my_func2", "params" : [] }]]}]])

    def test_recognise_method(self):
        data = tokenise_fsl("thing.my_meth()")
        self.assertEqual(data, [["expression", "thing"], ["method", {"name" : "my_meth", "params" : []}]])

    def test_recognise_method_1param(self):
        data = tokenise_fsl("thing.my_meth(arg1)")
        self.assertEqual(data, [["expression", "thing"], ["method", {"name" : "my_meth", "params" : [["expression", "arg1"]]}]])

    def test_recognise_method_Nparam(self):
        data = tokenise_fsl("thing.my_meth(arg1, arg2, arg3)")
        self.assertEqual(data, [["expression", "thing"], ["method", {"name" : "my_meth", "params" : [["expression", "arg1"], ["comma", ","], ["expression", "arg2"], ["comma", ","], ["expression", "arg3"]]}]])

    def test_recognise_nested_method(self):
        data = tokenise_fsl("thing.my_meth1(thing.my_meth2())")
        self.assertEqual(data, [["expression", "thing"], ["method", {"name" : "my_meth1", "params" : [ ["expression", "thing"], ["method", {"name" : "my_meth2", "params" : [] }]]}]])

    def test_recognise_operator(self):
        data = tokenise_fsl('+')
        self.assertEqual(data, [["operator", '+']])

    def test_recognise_unfinished_string(self):
        data = tokenise_fsl('"hello')
        self.assertEqual(data, [["string-semi", 'hello']])

    def test_recognise_attribute(self):
        data = tokenise_fsl('thing.name')
        self.assertEqual(data, [["expression", "thing"], ["attribute", "name"]])

    def test_recognise_colon(self):
        data = tokenise_fsl(':')
        self.assertEqual(data, [["colon", ":"]])

    def test_recognise_unfinished_bracket(self):
        data = tokenise_fsl('(1, 2')
        self.assertEqual(data, [["bracket_start", "("], ["int", "1"], ["comma", ","], ["int", "2"]])

    def test_recognise_colon(self):
        data = tokenise_fsl(':')
        self.assertEqual(data, [["colon", ":"]])
