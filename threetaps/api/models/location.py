""" threetaps.api.models.location

    This Python module implements the Location model object.
"""
#############################################################################

class Location:
    """ The Location class represents a location within the 3taps client APIs.

        A Location object currently has the following attributes:

            code

                A three-letter code uniquely identifying this location.

            countryRank

                An integer used to sort the countries into a useful order (for
                example, to place the United States at the top of the list of
                countries.

            country

                The name of the location's country, as a string.

            stateCode

                A brief (usually two-letter) code for the state or region this
                location is in.  This will be None for countries which do not
                have states or regions.

            stateName

                The name of the state or region this location is in.  This will
                be None for countries which do not have states or regions.

            cityRank

                An integer used to sort the cities within the country.

            city

                The name of the city within this country.

            hidden

                If True, the location should be hidden in the system's user
                interface.

            latitude

                The latitude of this location, as a floating-point number
                representing decimal degrees.

            longitude

                The longitude of this location, as a floating-point number
                representing decimal degrees.

        You can retrieve and change these attributes directly as required.

        WARNING:

            The structure of the Location object will change in the near
            future.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the Location object can be passed as
            keyword arguments if desired.
        """
        self.code        = kwargs.get("code")
        self.countryRank = kwargs.get("countryRank")
        self.country     = kwargs.get("country")
        self.stateCode   = kwargs.get("stateCode")
        self.stateName   = kwargs.get("stateName")
        self.cityRank    = kwargs.get("cityRank")
        self.city        = kwargs.get("city")
        self.hidden      = kwargs.get("hidden")
        self.latitude    = kwargs.get("latitude")
        self.longitude   = kwargs.get("longitude")

