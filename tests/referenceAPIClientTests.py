""" referenceAPIClientTests.py

    This Python module defines unit tests for the ReferenceAPIClient class.
"""
from threetaps.api import clients
from threetaps.api import models

import unittest

#############################################################################

class ReferenceAPIClientTestCase(unittest.TestCase):
    """ This class implements various unit tests for the ReferenceAPIClient.
    """
    def setUp(self):
        """ Prepare to run our unit tests.
        """
        self._api = clients.ReferenceAPIClient()
        self._api.enableLogging()


    def tearDown(self):
        """ Clean up after our unit tests.
        """
        self._api.disableLogging()
        self._api = None


    def testGetCategories(self):
        """ Test the ReferenceClient.getCategories() API call
        """
        response1 = self._api.getCategories(includeAnnotations=True)
        assert response1 != None
        assert len(response1) > 0

        response2 = self._api.getCategories(includeAnnotations=False)
        assert response2 != None
        assert len(response1) == len(response2)

        hasAnnotation1 = False
        hasAnnotation2 = False

        for category in response1:
            if len(category.annotations) > 0:
                hasAnnotation1 = True
                break

        for category in response2:
            if len(category.annotations) > 0:
                hasAnnotation2 = True
                break

        assert hasAnnotation1 == True
        assert hasAnnotation2 == False


    def testGetCategory(self):
        """ Test the ReferenceClient.getCategory() API call
        """
        response = self._api.getCategory("STVL", includeAnnotations=True)
        assert isinstance(response, models.Category)


    def testGetLocations(self):
        """ Test the ReferenceClient.getLocations() API call
        """
        response = self._api.getLocations()
        assert response != None
        assert len(response) > 0


    def testGetSources(self):
        """ Test the ReferenceClient.getSources() API call
        """
        response = self._api.getSources()
        assert response != None
        assert len(response) > 0

#############################################################################

def suite():
    """ Create and return a test suite with all the tests we need to run.
    """
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(ReferenceAPIClientTestCase)

