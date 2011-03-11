""" geocoderAPIClientTests.py

    This Python module defines unit tests for the GeocoderAPIClient class.
"""
from threetaps.api import clients

import unittest

#############################################################################

class GeocoderAPIClientTestCase(unittest.TestCase):
    """ This class implements the various unit tests for the GeocoderAPIClient.
    """
    def setUp(self):
        """ Prepare to run our unit tests.
        """
        self._api = clients.GeocoderAPIClient()
        self._api.enableLogging()


    def tearDown(self):
        """ Clean up after our unit tests.
        """
        self._api.disableLogging()
        self._api = None


    def testLatLong(self):
        """ Test the GeocoderClient.geocode() API call using a lat/long value
        """
        request = clients.GeocodeRequest()
        request.latitude  = 42.3496
        request.longitude = -71.0746

        response = self._api.geocode([request])

        assert len(response)         == 1
        assert response[0].code      == "HYA"
        assert response[0].latitude  == 42.3496
        assert response[0].longitude == -71.0746


    def testCity(self):
        """ Test the GeocoderClient.geocode() API call using a city name
        """
        request = clients.GeocodeRequest()
        request.city = "Hong Kong"

        response = self._api.geocode([request])

        assert len(response)         == 1
        assert response[0].code      == "HKG"
        assert response[0].latitude  == 22.28552
        assert response[0].longitude == 114.15769


    def testState(self):
        """ Test the GeocoderClient.geocode() API call using a state name
        """
        request = clients.GeocodeRequest()
        request.state = "California"

        response = self._api.geocode([request])

        assert len(response)         == 1
        assert response[0].code      == "CAZ"
        assert response[0].latitude  == 37.25022
        assert response[0].longitude == -119.75126


    def testCountry(self):
        """ Test the GeocoderClient.geocode() API call using a country name
        """
        request = clients.GeocodeRequest()
        request.country = "New Zealand"

        response = self._api.geocode([request])

        assert len(response)         == 1
        assert response[0].code      == "NZL"
        assert response[0].latitude  == -42
        assert response[0].longitude == 174


    def testStructuredAddress(self):
        """ Test the GeocoderClient.geocode() API call using a full address
        """
        request = clients.GeocodeRequest()
        request.country  = "United States"
        request.state    = "California"
        request.city     = "San Francisco"
        request.locality = "Sausalito"
        request.street   = "66 Starbuck Drive, Muir Beach"

        response = self._api.geocode([request])

        assert len(response)         == 1
        assert response[0].code      == "SFO"
        assert response[0].latitude  == 37.85909
        assert response[0].longitude == -122.48525


    def testZIPCode(self):
        """ Test the GeocoderClient.geocode() API call using a ZIP code
        """
        request = clients.GeocodeRequest()
        request.postal = "94965"

        response = self._api.geocode([request])

        assert len(response)         == 1
        assert response[0].code      == "SFO"
        assert response[0].latitude  == 37.84723
        assert response[0].longitude == -122.53114


    def testFreeformText(self):
        """ Test the GeocoderClient.geocode() API call using freeform text
        """
        request = clients.GeocodeRequest()
        request.text = "66 Starbuck Drive, Muir Beach, Sausalito, USA"

        response = self._api.geocode([request])

        assert len(response)         == 1
        assert response[0].code      == "SFO"
        assert response[0].latitude  == 37.85909
        assert response[0].longitude == -122.48525

#############################################################################

def suite():
    """ Create and return a test suite with all the tests we need to run.
    """
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(GeocoderAPIClientTestCase)

