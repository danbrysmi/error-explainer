from django.test import TestCase
from results.models import ErrorTemplate, ErrorType
from results.views import extract_example, match_template
# Create your tests here.

#################
# MODEL TESTING #
#################
class ErrorTemplateTestCase(TestCase):
    def setUp(self):
        self.e_type = ErrorType.objects.create(name="NewError")
        self.unk_e_type = ErrorType.objects.create(name="Unknown")
        ErrorTemplate.objects.create(template-"Error not found", error_type = self.unk_e_type)
        ErrorTemplate.objects.create(template="NewError: <1> is wrong.", error_type = self.e_type)

    def test_filter_by_error(self):
        """Errors are correctly filtered by type."""
        new_errors = ErrorTemplate.objects.filter(error_type=self.e_type)
        self.assertEqual(len(new_errors), 1)

    def test_invalid_error(self):
        """Invalid Errors are given the Unknown Error class."""
        trace = "not sure what this error is"
        temp = match_template(trace, self.unk_e_type)
        self.assertEqual(temp.error_type, "Unknown")
        # need to edit match_template function so it only has the error_trace function, it should automatically detect what type of error it is, giving Unknown if not recognised.

#################
# VIEW TESTING #
#################
class SolveViewTestCase(TestCase):
    def test_extract_param_on_testcase(self):
        """Test that example python code is extracted"""
        example = extract_example("testcase")
        self.assertEqual(example, '# this is a test\nprint("Eggs")\n')

    def test_extract_param_invalid_tag(self):
        """Test that False is returned with an unknown tag"""
        example = extract_example("eggs")
        self.assertEqual(example, False)
