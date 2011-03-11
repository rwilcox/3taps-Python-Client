""" threetaps.api.models.source

    This Python module implements the Source model object.
"""
#############################################################################

class Source:
    """ The Source class represents a data source within the 3taps client APIs.

        A Source object has the following attributes:

            name

                The name of the data source, as a string.

            code

                A brief string uniquely identifying this data source.

            logoURL

                The URL used to access this data source's logo, as a string.

            smallLogoURL

                The URL used to access the small version of this data source's
                logo, as a string.

        You can retrieve and change these attributes directly as required.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the Source object can be passed as
            keyword arguments if desired.
        """
        self.name         = kwargs.get("name")
        self.code         = kwargs.get("code")
        self.logoURL      = kwargs.get("logoURL")
        self.smallLogoURL = kwargs.get("smallLogoURL")

