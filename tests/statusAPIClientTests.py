""" statusAPIClientTests.py

    This Python module defines unit tests for the StatusAPIClient class.
"""
from threetaps.api import clients
from threetaps.api import models

import time
import unittest

#############################################################################

class StatusAPIClientTestCase(unittest.TestCase):
    """ This class implements the various unit tests for the StatusAPIClient.
    """
    def setUp(self):
        """ Prepare to run our unit tests.
        """
        self._api = clients.StatusAPIClient()
        self._api.enableLogging()


    def tearDown(self):
        """ Clean up after our unit tests.
        """
        self._api.disableLogging()
        self._api = None


    def testPostingStatus(self):
        """ Test the StatusClient.update() and StatusClient.get() calls
        """
        # Start by creating a dummy "posting" that we can create status updates
        # for.

        source     = "CRAIG"
        externalID = "TEST" + str(time.time())

        # Send in a status update for our dummy posting.

        event = {'status'     : "found",
                 'externalID' : externalID,
                 'source'     : source}

        response = self._api.update([event])

        assert response != None
        assert response['success'] == True

        # Send in a second status update.

        event = {'status'     : "got",
                 'externalID' : externalID,
                 'source'     : source}

        response = self._api.update([event])

        assert response != None
        assert response['success'] == True

        # Finally, retrieve the status updates for our dummy posting.

        posting = models.Posting(source=source, externalID=externalID)

        response = self._api.get([posting])

        assert response != None
        assert len(response) == 1

        assert response[0]['exists']       == True
        assert response[0]['externalID']   == externalID
        assert response[0]['source']       == source
        assert len(response[0]['history']) == 2


    def testSystemStatus(self):
        """ Test the StatusClient.system() call
        """
        response = self._api.system()
        assert response != None
        assert "code" in response
        assert "message" in response

#############################################################################

def suite():
    """ Create and return a test suite with all the tests we need to run.
    """
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(StatusAPIClientTestCase)

