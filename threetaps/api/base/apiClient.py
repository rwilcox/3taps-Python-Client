""" threetaps.api.base.apiClient

    This Python module implements the APIClient class.
"""
from threetaps.api.base import constants

import logging
import urllib

#############################################################################

class APIClient:
    """ The base class used to define a 3taps API client.

        All of our API client objects are derived from this base class.
    """
    def __init__(self, url=constants.DEFAULT_API_URL,
                       port=constants.DEFAULT_API_PORT):
        """ Standard initializer.

            The API client will use the given URL and HTTP port to access the
            3taps APIs.
        """
        self._url         = url
        self._port        = port
        self._logRequests = False


    def enableLogging(self):
        """ Turn on logging of HTTP requests.

            If this is turned on, information about each HTTP request that is
            made, including the URL, the supplied parameters, and the type of
            response that was received, will be sent to the Python standard
            library's logging module as INFO messages.
        """
        self._logRequests = True


    def disableLogging(self):
        """ Turn off logging of HTTP requests.
        """
        self._logRequests = False


    def sendRequest(self, endpoint, type="GET", **params):
        """ Send an HTTP request to the 3taps API.

            The parameters are as follows:

                endpoint

                    A string that defines the URL to access, relative to our
                    base URL and HTTP port.

                type

                    The type of HTTP request to make.  The following values are
                    supported:

                        GET
                        POST

            The remaining keyword parameters (if any) are passed as query
            parameters to the URL.

            Upon completion, we return a dictionary with the following entries:

                status

                    The HTTP status code returned by the server.

                contents

                    The unprocessed text returned by the server.

                content-type

                    The HTTP content-type value returned by the server.

            If a connection cannot be made to the server, we return None.
        """
        url = self._url + ":" + str(self._port) + "/" + endpoint

        postData = None # initially.

        if type == "GET":
            if len(params) > 0:
                url = url + "?" + urllib.urlencode(params)
        elif type == "POST":
            if len(params) > 0:
                postData = urllib.urlencode(params)
        else:
            raise RuntimeError("Illegal HTTP type parameter: " + repr(type))

        if self._logRequests:
            if postData != None:
                logging.info("HTTP %s %s - %s" % (type, url, postData))
            else:
                logging.info("HTTP %s %s" % (type, url))

        try:
            connection = urllib.urlopen(url, postData)
        except IOError,e:
            if self._logRequests:
                logging.error(repr(e))
            return None

        status      = connection.code
        contents    = connection.read()
        contentType = connection.info().gettype()

        connection.close()

        if self._logRequests:
            logging.info(" -> status=%d, content-type=%s, contents=%d bytes" %
                         (status, contentType, len(contents)))

        return {'status'       : status,
                'contents'     : contents,
                'content-type' : contentType}

