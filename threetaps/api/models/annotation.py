""" threetaps.api.models.annotation

    This Python module implements the Annotation model object.
"""
#############################################################################

class Annotation:
    """ The Annotation class represents an annotation within the 3taps client
        APIs.

        An Annotation object has the following attributes:

            name

                The name of this annotation.

            type

                A string identifying the type of annotation.  The following
                annotation types are currently supported:

                    select
                    string
                    number

            options

                For annotations of type "select", this will be a list of the
                possible options supported by this annotation.  Each item in
                this list should be an AnnotationOption object.

        You can retrieve and change these attributes directly as required.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the Annotation object can be passed as
            keyword arguments if desired.
        """
        self.name    = kwargs.get("name")
        self.type    = kwargs.get("type")
        self.options = kwargs.get("options")

#############################################################################

class AnnotationOption:
    """ This class represents a single option for an Annotation.

        The AnnotationOption object has the following attributes:

            value

                A string containing the value for this annotation option.

            subAnnotation

                If defined, this is an Annotation object representing the
                sub-annotation for this option.
    """
    def __init__(self, **kwargs):
        """ Standard initializer.

            The initial attributes for the AnnotationOption object can be
            passed as keyword arguments if desired.
        """
        self.value         = kwargs.get("value")
        self.subAnnotation = kwargs.get("subAnnotation")

