from django.test import TestCase
from results.models import ErrorTemplate, ErrorType

# Create your tests here.

#################
# MODEL TESTING #
#################
class ErrorTemplateTestCase(TestCase):
    def setUp(self):
        self.e_type = ErrorType.objects.create(name="NewError")
        ErrorTemplate.objects.create(template="NewError: <1> is wrong.", error_type = self.e_type)

    def test_filter_by_error(self):
        """Errors are correctly filtered by type."""
        new_errors = ErrorTemplate.objects.filter(error_type=self.e_type)
        self.assertEqual(len(new_errors), 1)
