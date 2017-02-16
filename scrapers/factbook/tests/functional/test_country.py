from home.tests import *

class TestCountryController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='country', action='index'))
        # Test response...
