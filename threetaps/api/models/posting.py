""" threetaps.api.models.posting

    This Python module implements the Posting model object.
"""
#############################################################################

class Posting:
    """ The Posting class represents a posting within the 3taps client APIs.

        A Posting object has the following attributes:

            postKey

                A string uniqely identifying this posting in the 3taps system.

            location

                The code for the location to be associated with this posting,
                as a string.

            category

                The code for the category to be associated with this posting,
                as a string.

            source

                The code for the data source to be associated with this
                posting, as a string.

            heading

                A string representing a brief summary of the posting, up to 255
                characters long.

            body

                A string containing the full text of the posting, up to 5,000
                character long.

            latitude

                The latitude value associated with this posting, if any.  If
                this is given, it will be a floating-point number representing
                the posting's latitude in decimal degrees.

            longitude

                The longitude value associated with this posting, if any.  If
                this is given, it will be a floating-point number representing
                the posting's longitude in decimal degrees.

            language

                A two-character code identifying the language of the posting.
                The value used here should be a valid ISO 6943-1 language code.

            price

                The price to associate with this posting, as a floating-point
                number.

            currency

                A three-character code identifying which currency the price is
                in.  If supplied, this must match one of the valid ISO 4217
                currency codes.

            images

                A list of images to be associated with this posting.  Each list
                item will be the URL of the image to display.

            externalID

                A string containing additional information that identifies this
                posting in some external system.

            externalURL

                A string containing the URL that refers to this posting in some
                external system.

            accountName

                The name of the author of this posting in the originating
                system, if known.

            accountID

                The ID of the author in the originating system, as a string.
                Note that in many cases the account name and the account ID
                will be the same.

            timestamp

                A datetime.datetime object representing the date and time at
                which this posting was made.  Note that the date and time will
                be in UTC.

            expiration

                A datetime.datetime object representing the date and time at
                which this posting will expire, if specified.  Note that the
                date and time will be in UTC.

            annotations

                A dictionary mapping annotation names to values for this
                posting's untrusted annotations.

            trustedAnnotations

                A dictionary mapping annotation names to values for this
                posting's trusted annotations.

            clickCount

                The number of times this posting has been clicked on in the
                3taps system.

        You can retrieve and change these attributes directly as required.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the Posting object can be passed as
            keyword arguments if desired.
        """
        self.postKey            = kwargs.get("postKey")
        self.location           = kwargs.get("location")
        self.category           = kwargs.get("category")
        self.source             = kwargs.get("source")
        self.heading            = kwargs.get("heading")
        self.body               = kwargs.get("body")
        self.latitude           = kwargs.get("latitude")
        self.longitude          = kwargs.get("longitude")
        self.language           = kwargs.get("language")
        self.price              = kwargs.get("price")
        self.currency           = kwargs.get("currency")
        self.images             = kwargs.get("images", [])
        self.externalID         = kwargs.get("externalID")
        self.externalURL        = kwargs.get("externalURL")
        self.accountName        = kwargs.get("accountName")
        self.accountID          = kwargs.get("accountID")
        self.timestamp          = kwargs.get("timestamp")
        self.expiration         = kwargs.get("expiration")
        self.annotations        = kwargs.get("annotations", {})
        self.trustedAnnotations = kwargs.get("trustedAnnotations", {})
        self.clickCount         = kwargs.get("clickCount")

