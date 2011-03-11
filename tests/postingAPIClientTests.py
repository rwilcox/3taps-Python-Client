""" postingAPIClientTests.py

    This Python module defines unit tests for the PostingAPIClient class.
"""
from threetaps.api import clients
from threetaps.api import models

import datetime
import time
import unittest

#############################################################################

class PostingAPIClientTestCase(unittest.TestCase):
    """ This class implements the various unit tests for the PostingAPIClient.

        Note that we only need one test case to completely test the
        PostingAPIClient's API calls.  This is because create() calls
        createMany(), update() calls updateMany(), and delete() calls
        deleteMany().  There's no real point in creating a separate test for
        these API calls, since they've already been tested by the testSingle()
        test case.
    """
    def setUp(self):
        """ Prepare to run our unit tests.
        """
        self._api = clients.PostingAPIClient()
        self._api.enableLogging()


    def tearDown(self):
        """ Clean up after our unit tests.
        """
        self._api.disableLogging()
        self._api = None


    def testSingle(self):
        """ Test the PostingClient.create(), update() and delete() API calls

        """
        # Create a new posting.

        posting = models.Posting(location="SFO",
                                 source="CRAIG",
                                 heading="Test Post",
                                 externalID = "TEST" + str(time.time()),
                                 timestamp=datetime.datetime.utcnow())

        response = self._api.create(posting)

        assert response != None
        if "error" in response:
            self.fail(repr(response['error']))
        assert "postKey" in response

        postKey = response['postKey']

        # Update the posting.

        update = models.Posting(postKey=postKey,
                                body="Body of test post")

        success = self._api.update(update)

        assert success == True

        # Delete the posting.

        success = self._api.delete(postKey)

        assert success == True

#############################################################################

def suite():
    """ Create and return a test suite with all the tests we need to run.
    """
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(PostingAPIClientTestCase)

