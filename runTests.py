""" runTests.py

    This Python program runs the various unit tests defined in the 'tests'
    package.
"""
import tests.geocoderAPIClientTests
import tests.postingAPIClientTests
import tests.referenceAPIClientTests
import tests.searchAPIClientTests
import tests.statusAPIClientTests

import logging
import unittest

#############################################################################

def runTests():
    """ Run the various unit tests.
    """
#    logging.basicConfig(level=logging.INFO) # Show API requests.

    allTests = unittest.TestSuite()
    allTests.addTest(tests.geocoderAPIClientTests.suite())
    allTests.addTest(tests.postingAPIClientTests.suite())
    allTests.addTest(tests.referenceAPIClientTests.suite())
    allTests.addTest(tests.searchAPIClientTests.suite())
    allTests.addTest(tests.statusAPIClientTests.suite())

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(allTests)

#############################################################################

if __name__ == "__main__":
    runTests()

