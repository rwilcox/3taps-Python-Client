""" threetaps.api.clients.searchAPIClient

    This Python module implements the 3taps Search API client object.
"""
from threetaps.api.base   import APIClient
from threetaps.api.models import Posting

import urllib
import simplejson as json

#############################################################################

class SearchAPIClient(APIClient):
    """ A client for the 3taps Search API.
    """
    def search(self, query, rpp=None, page=None, retvals=None):
        """ Perform a search against the 3taps posting database.

            The parameters are as follows:

                query

                    A SearchQuery object defining the parameters of the search.
                    Only postings which match the search query will be
                    returned.

                rpp

                    The number of results to return per page.  If this is not
                    specified, a maximum of ten postings will be returned.  If
                    this is set to -1, all matching postings will be returned.

                page

                    The page number of the results to return, where zero is the
                    most recent page.  If this is not specified, the most
                    recent page of results will be returned.

                retvals

                    A list of field names to return for each matching posting.
                    The following field names are currently supported:

                        source
                        category
                        location
                        longitude
                        latitude
                        heading
                        body
                        images
                        externalURL
                        userID
                        timestamp
                        externalID
                        annotations
                        postKey

                    If the 'retvals' argument is not supplied, the following
                    default set of fields will be returned:

                        category
                        location
                        heading
                        externalURL
                        timestamp

            Upon completion, we return a dictionary with the following entries:

                success

                    If the search succeeded, this will be set to True.

                numResults

                    The total number of postings found by this search.

                execTimeMs

                    The amount of time it took the 3taps server to perform this
                    search, in milliseconds.

                error

                    If the search did not succeed (success=False), this will be
                    a string explaining why the search failed.

                results

                    A list of matching postings.  Each item in this list will
                    be a Posting object containing the returned details of the
                    matching posting.
        """
        params = self._queryToParamsDict(query)

        if rpp     != None: params['rpp']     = str(rpp)
        if page    != None: params['page']    = str(page)
        if retvals != None: params['retvals'] = ",".join(retvals)

        response = self.sendRequest("search", **params)

        if (response == None) or (response['status'] != 200):
            return {'success' : False,
                    'error'   : "Unable to connect to 3taps Search API"}

        results = json.loads(response['contents'])

        if not results['success']:
            return {'success' : False,
                    'error'   : results['error']}

        postings = []

        for row in results['results']:
            postings.append(Posting(**row))

        return {'success'    : True,
                'numResults' : results['numResults'],
                'execTimeMs' : results['execTimeMs'],
                'results'    : postings}


    def range(self, query, fields):
        """ Calculate the minimum and maximum field values for a search.

            The parameters are as follows:

                query

                    A SearchQuery object defining the parameters for a search.

                fields

                    A list of field names to calculate the range for.

            The 3taps server will attempt to calculate the minimum and maximum
            value for each of the specified fields, across all postings that
            match the given search query.

            Upon completion, we return a dictionary mapping field names to a
            (minValue,maxValue) tuple for that field.  Note that the minimum
            and/or maximum value will be set to None if no value could be
            calculated.

            If an error occurs (for example, because the server could not be
            contacted), we return None.
        """
        params = self._queryToParamsDict(query)
        params['fields'] = ",".join(fields)

        response = self.sendRequest("search/range", **params)

        if (response == None) or (response['status'] != 200):
            return None

        results = json.loads(response['contents'])

        ranges = {}
        for field in fields:
            minValue = None
            maxValue = None
            if field in results:
                minValue = results[field].get("min")
                maxValue = results[field].get("max")
            ranges[field] = (minValue, maxValue)

        return ranges


    def summary(self, query, dimension):
        """ Calculate the number of matching postings across a given dimension.

            The parameters are as follows:

                query

                    A SearchQuery object defining the parameters for a search.

                dimension

                    The name of a field to calculate the summary across.  The
                    following dimension values are currently supported:

                        source
                        category
                        location

            Upon completion, we return a dictionary with the following entries:

                totals

                    A dictionary mapping the dimension value to the total
                    number of matching postings for that value.

                execTimeMs

                    The number of milliseconds it took to calculate the
                    summary.

            If an error occurs (for example, because the server could not be
            contacted), we return None.
        """
        params = self._queryToParamsDict(query)
        params['dimension'] = dimension

        response = self.sendRequest("search/summary", **params)

        if (response == None) or (response['status'] != 200):
            return None

        results = json.loads(response['contents'])
        return results


    def count(self, query):
        """ Calculate the number of postings which match a given search query.

            'query' is a SearchQuery object defining the parameters of a
            search.  We return the number of postings which match that search
            query, or None if the server cannot be contacted.
        """
        params = self._queryToParamsDict(query)

        response = self.sendRequest("search/count", **params)

        if (response == None) or (response['status'] != 200):
            return None

        results = json.loads(response['contents'])
        return results['count']


    def bestMatch(self, keywords):
        """ Calculate the 3taps category that best matches a set of keywords.

            'keywords' should be a list of strings containing keywords that we
            want to find the best match for.  We ask the 3taps server to
            identify the category which best matches those keywords.

            Upon completion, we return a dictionary with the following entries:

                category

                    The category code which best matches the given keywords.

                numResults

                    The number of postings which belong to that category.

            Note that if an error occurs, we return None.
        """
        response = self.sendRequest("search/bestMatch",
                                    keywords=",".join(keywords))

        if (response == None) or (response['status'] != 200):
            return None

        results = json.loads(response['contents'])
        return results

    # =====================
    # == PRIVATE METHODS ==
    # =====================

    def _queryToParamsDict(self, query):
        """ Convert a SearchQuery object to a search parameters dictionary.

            We create a dictionary with key/value entries matching the contents
            of the given SearchQuery object.
        """
        params = {}
        if query.source != None:
            params['source'] = query.source
        if query.category != None:
            params['category'] = query.category
        if query.location != None:
            params['location'] = query.location
        if query.heading != None:
            params['heading'] = urllib.quote_plus(query.heading)
        if query.body != None:
            params['body'] = urllib.quote_plus(query.body)
        if query.text != None:
            params['text'] = urllib.quote_plus(query.text)
        if query.externalID != None:
            params['externalID'] = query.externalID
        if query.start != None:
            params['start'] = query.start.strftime("%Y/%m/%d %H:%M:%S UTC")
        if query.end != None:
            params['end'] = query.end.strftime("%Y/%m/%d %H:%M:%S UTC")
        if query.annotations != None:
            params['annotations'] = json.dumps(query.annotations)
        if query.trustedAnnotations != None:
            params['trustedAnnotations'] = json.dumps(query.trustedAnnotations)
        return params

#############################################################################

class SearchQuery:
    """ This class encapsulates a query against the 3taps Search API.

        A SearchQuery object can have the following attributes:

            source

                The 5-characgter source code a posting must have if it is to be
                included in the list of search results.

            category

                The 4-character category code a posting must have if it is to
                be included in the list of search results.  Note that multiple
                categories can be searched by passing in multiple category
                codes, separated by +OR+.

            location

                The 3-character location code a posting must have if it is to
                be included in the list of search results.  Note that multiple
                locations can be searched by passing in multiple location
                codes, separated by +OR+.

            heading

                A string which must occur in the heading of the posting if it
                is to be included in the list of search results.

            body

                A string which must occur in the body of the posting if it is
                to be included in the list of search results.

            text

                A string which must occur in either the heading or the body of
                the posting if it is to be included in the list of search
                results.

            externalID

                A string which must match the "externalID" field for a postig
                if it is to be included in the list of search results.

            start

                A datetime.datetime object defining the desired starting
                timeframe for the search query.  Only postings with a timestamp
                greater than or equal to the given value will be included in
                the list of search results.  Note that the specified time and
                date must be in UTC.

            end

                A datetime.datetime object defining the desired ending
                timeframe for the search query.  Only postings with a timestamp
                less than or equal to the given value will be included in
                the list of search results.  Note that the specified time and
                date must be in UTC.

            annotations

                A dictionary of key/value pairs that a posting must have in its
                annotations to be included in the list of search results.

            trustedAnnotations

                A dictionary of key/value pairs that a posting must have in its
                trusted annotations to be included in the list of search
                results.

        You can retrieve and change these attributes directly as required.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the SearchQuery object can be passed
            as keyword arguments if desired.
        """
        self.source             = kwargs.get("source")
        self.category           = kwargs.get("category")
        self.location           = kwargs.get("location")
        self.heading            = kwargs.get("heading")
        self.body               = kwargs.get("body")
        self.text               = kwargs.get("text")
        self.externalID         = kwargs.get("externalID")
        self.start              = kwargs.get("start")
        self.end                = kwargs.get("end")
        self.annotations        = kwargs.get("annotations")
        self.trustedAnnotations = kwargs.get("trustedAnnotations")

