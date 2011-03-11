""" threetaps.api.clients.geocoderAPIClient

    This Python module implements the 3taps Geocoder API client object and
    related classes.
"""
from threetaps.api.base import APIClient

import simplejson as json

#############################################################################

class GeocoderAPIClient(APIClient):
    """ A client for the 3taps Geocoder API.
    """
    def geocode(self, requests, agentID=None, authID=None):
        """ Ask the geocoder to geocode one or more postings.

            The parameters are as follows:

                'requests'
                
                    A list of GeocodeRequest objects containing the location
                    information for one or more postings.

                'agentID'

                    A string identifying the entity which is sending this
                    request.

                'authID'

                    A string which authorizes this entity to make the given
                    request.

            Note that the 'agentID' and 'authID' values are currently ignored.

            Upon completion, we return a list of GeocodeResponse objects, one
            for each entry in the 'requests' list.
        """
        data = []
        for request in requests:
            posting = {}
            if request.latitude != None:
                posting['latitude'] = request.latitude
            if request.longitude != None:
                posting['longitude'] = request.longitude
            if request.country != None:
                posting['country'] = request.country
            if request.state != None:
                posting['state'] = request.state
            if request.city != None:
                posting['city'] = request.city
            if request.locality != None:
                posting['locality'] = request.locality
            if request.street != None:
                posting['street'] = request.street
            if request.postal != None:
                posting['postal'] = request.postal
            if request.text != None:
                posting['text'] = request.text
            data.append(posting)

        args = {}
        if agentID != None:
            args['agentID'] = agentID
        if authID != None:
            args['authID'] = authID
        args['data'] = json.dumps(data)

        response = self.sendRequest("geocoder/geocode", "POST", **args)

        if (response == None) or (response['status'] != 200):
            # An error occurred -> can't geocode anything.
            responses = []
            for i in range(len(requests)):
                responses.append(GeocodeResponse())
            return responses

        results = json.loads(response['contents'])

        responses = []
        for code,latitude,longitude in results:
            responses.append(GeocodeResponse(code=code,
                                             latitude=latitude,
                                             longitude=longitude))
        return responses

#############################################################################

class GeocodeRequest:
    """ An object encapsulating a single geocoding request to the server.

        A GeocoderRequest object has the following attributes:

            latitude

                The latitude of the posting, as a floating-point number in
                decimal degrees.

            longitude

                The longitude of the posting, as a floating-point number in
                decimal degrees.

            country

                The name of the country.

            state

                The name or code for the state or region.

            city

                The name of the city.

            locality

                The name of a suburb, area or town within the specified city.

            street

                The full street address for this location.

            postal

                The ZIP or postal code for this location.

            text

                Freeform text holding a location name or address value.

        You can retrieve and change these attributes directly as required.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the GeocoderRequest object can be passed
            as keyword arguments if desired.
        """
        self.latitude  = kwargs.get("latitude")
        self.longitude = kwargs.get("latitude")
        self.country   = kwargs.get("country")
        self.state     = kwargs.get("state")
        self.city      = kwargs.get("city")
        self.locality  = kwargs.get("locality")
        self.street    = kwargs.get("street")
        self.postal    = kwargs.get("postal")
        self.text      = kwargs.get("text")

#############################################################################

class GeocodeResponse:
    """ An object encapsulating a single geocoding response from the server.

        A GeocoderResponse object has the following attributes:

            code

                The 3taps location code for this posting, or None if the
                posting could not be geocoded.

            latitude

                The calculated latitude of the posting, as a floating-point
                number in decimal degrees.  This will be set to None if the
                latitude of the posting could not be calculated.

            longitude

                The calculated longitude of the posting, as a floating-point
                number in decimal degrees.  This will be set to None if the
                longitude of the posting could not be calculated.

        You can retrieve and change these attributes directly as required.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the GeocoderResponse object can be
            passed as keyword arguments if desired.
        """
        self.code      = kwargs.get("code")
        self.latitude  = kwargs.get("latitude")
        self.longitude = kwargs.get("longitude")

