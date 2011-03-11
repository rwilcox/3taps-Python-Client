""" __init__.py

    threetaps.api.models package initialization file.

    Note that we load the various model objects into the threetaps.api.models
    namespace, to make them easier to access.
"""
from threetaps.api.models.annotation import Annotation
from threetaps.api.models.annotation import AnnotationOption
from threetaps.api.models.category   import Category
from threetaps.api.models.location   import Location
from threetaps.api.models.posting    import Posting
from threetaps.api.models.source     import Source
