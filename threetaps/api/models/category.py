""" threetaps.api.models.category

    This Python module implements the Category model object.
"""
#############################################################################

class Category:
    """ The Category class represents a category within the 3taps client APIs.

        A Category object has the following attributes:

            code

                A brief string uniquely identifying this category.

            group

                A string identifying the group this Category belongs to.

            name

                A string containing the name of this category.

            annotations

                A list of Annotation objects for the annotations associated
                with this category.

        You can retrieve and change these attributes directly as required.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the Category object can be passed as
            keyword arguments if desired.
        """
        self.code        = kwargs.get("code")
        self.group       = kwargs.get("group")
        self.name        = kwargs.get("name")
        self.annotations = kwargs.get("annotations", [])

