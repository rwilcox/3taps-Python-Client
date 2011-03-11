""" searchAPIClientTests.py

    This Python module defines unit tests for the SearchAPIClient class.
"""
from threetaps.api import clients
from threetaps.api import models

import unittest

#############################################################################

class SearchAPIClientTestCase(unittest.TestCase):
    """ This class implements the various unit tests for the SearchAPIClient.
    """
    def setUp(self):
        """ Prepare to run our unit tests.
        """
        self._api = clients.SearchAPIClient()
        self._api.enableLogging()


    def tearDown(self):
        """ Clean up after our unit tests.
        """
        self._api.disableLogging()
        self._api = None


    def testSearch(self):
        """ Test the SearchClient.search() API call
        """
        query = clients.SearchQuery(source="CRAIG", location="SFO",
                                    text="bike")

        response = self._api.search(query)

        assert response != None
        assert response['success'] == True
        assert len(response['results']) > 0
        assert len(response['results']) <= response['numResults']


    def testRange(self):
        """ Test the SearchClient.range() API call
        """
        query = clients.SearchQuery(source="CRAIG", location="SFO",
                                    text="bike")

        response = self._api.range(query, ["price"])

        assert response != None
        assert "price" in response
        assert response['price'] != None
        minValue,maxValue = response['price']
        assert minValue != None
        assert maxValue != None
        assert minValue <= maxValue


    def testSummary(self):
        """ Test the SearchClient.summary() API call
        """
        query = clients.SearchQuery(source="CRAIG", location="SFO",
                                    text="bike")
        
        response = self._api.summary(query, "category")

        assert response != None
        assert len(response['totals']) > 0


    def testCount(self):
        """ Test the SearchClient.count() API call
        """
        query = clients.SearchQuery(source="CRAIG", location="SFO",
                                    text="bike")
        
        total = self._api.count(query)

        assert total != None
        assert total > 0


    def testBestMatch(self):
        """ Test the SearchClient.bestMatch() API call
        """
        response = self._api.bestMatch(["iPad"])

        assert response != None
        assert "category" in response
        assert response['category'] == "SCOM"
        assert "numResults" in response
        assert response['numResults'] > 0

#############################################################################

def suite():
    """ Create and return a test suite with all the tests we need to run.
    """
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(SearchAPIClientTestCase)

