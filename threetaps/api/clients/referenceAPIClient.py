""" threetaps.api.clients.referenceAPIClient

    This Python module implements the 3taps Reference API client object.
"""
from threetaps.api.base   import APIClient
from threetaps.api.models import Category, Annotation, AnnotationOption
from threetaps.api.models import Location
from threetaps.api.models import Source

import simplejson as json

#############################################################################

class ReferenceAPIClient(APIClient):
    """ A client for the 3taps Reference API.
    """
    def getCategories(self, includeAnnotations=True):
        """ Return the master list of all known 3taps categories.

            We download and return a list of Category objects corresponding to
            the master list of all known 3taps categories.  If
            'includeAnnotations' is True (the default), the annotation details
            will also be downloaded.

            If the list of categories cannot be downloaded for some reason, we
            return None.
        """
        if includeAnnotations:
            request = "reference/category?annotations=true"
        else:
            request = "reference/category?annotations=false"

        response = self.sendRequest(request)

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])

        categories = []
        for cat in results:
            category = self._parseCategory(cat)
            categories.append(category)

        return categories


    def getCategory(self, categoryCode, includeAnnotations=True):
        """ Return the details of a single 3taps category.

            We return a Category object corresponding to the 3taps category
            with the given code.  If 'includeAnnotations' is True (the
            default), the annotation details will also be included.

            If the category does not exist, or some problem occurs while
            downloading the category details, we return None.
        """
        if includeAnnotations:
            request = "reference/category/"+categoryCode+"?annotations=true"
        else:
            request = "reference/category/"+categoryCode+"?annotations=false"

        response = self.sendRequest(request)

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])
        if len(results) != 1:
            return None # Should never happen.

        return self._parseCategory(results[0])


    def getLocations(self):
        """ Return the master list of all known 3taps locations.

            We download and return a list of Location objects corresponding to
            the master list of all known 3taps locations.  If the list of
            locations cannot be downloaded for some reason, we return None.
        """
        response = self.sendRequest("reference/location")

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])

        locations = []
        for loc in results:
            locations.append(self._parseLocation(loc))

        return locations


    def getSources(self):
        """ Return the master list of all known 3taps sources.

            We download and return a list of Source objects corresponding to
            the master list of all known 3taps data sources.  If the list of
            sources cannot be downloaded for some reason, we return None.
        """
        response = self.sendRequest("reference/source")

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])

        sources = []
        for src in results:
            sources.append(self._parseSource(src))

        return sources

    # =====================
    # == PRIVATE METHODS ==
    # =====================

    def _parseCategory(self, data):
        """ Convert the JSON-format category data into a Category object.

            'data' should be a dictionary with one or more of the following
            entries:

                "group"
                "category"
                "code"
                "annotations"

            If it exists, the "annotations" entry should be a list of
            annotations for this category, where each list item is itself a
            dictionary with one or more of the following entries:

                "name"
                "type"
                "options"

            'options' should be a list of annotation options, where each item
            in this list is a dictionary with one or more of the following
            entries:

                "value"
                "subannotation"

            Note that 'data' will be in the format received from the 3taps
            server after decoding the JSON-format data.

            We convert 'data' into a Category object, which we then return to
            the caller.
        """
        category = Category()
        if "code"     in data: category.code  = data['code']
        if "category" in data: category.name  = data['category']
        if "group"    in data: category.group = data['group']
        if "annotations" in data:
            category.annotations = []
            for ann in data['annotations']:
                category.annotations.append(self._parseAnnotation(ann))
        return category


    def _parseAnnotation(self, data):
        """ Convert the JSON-format annotation data into an Annotation object.

            'data' should be a dictionary with one or more of the following
            entries:

                "name"
                "type"
                "options"

            'options' should be a list of annotation options, where each item
            in this list is a dictionary with one or more of the following
            entries:

                "value"
                "subannotation"

            Note that 'data' will be in the format received from the 3taps
            server after decoding the JSON-format data.

            We convert 'data' into an Annotation object, which we then return
            to the caller.
        """
        annotation = Annotation()
        if "name" in data: annotation.name = data['name']
        if "type" in data: annotation.type = data['type']
        if "options" in data:
            annotation.options = []
            for opt in data['options']:
                option = AnnotationOption()
                if "value" in opt: option.value = opt['value']
                if "subannotation" in opt:
                    subAnnotation = self._parseAnnotation(opt['subannotation'])
                    option.subAnnotation = subAnnotation
                annotation.options.append(option)
        return annotation


    def _parseLocation(self, data):
        """ Convert the JSON-format location data into a Location object.

            'data' should be a dictionary with one or more of the following
            entries:

                "code"
                "countryRank"
                "country"
                "cityRank"
                "city"
                "stateCode"
                "stateName"
                "hidden"
                "latitude"
                "longitude"

            Note that this is the format received from the 3taps server after
            decoding the JSON-format data.

            We convert 'data' into a Location object, which we then return to
            the caller.
        """
        location = Location()
        if "code"        in data: location.code        = data['code']
        if "countryRank" in data: location.countryRank = data['countryRank']
        if "country"     in data: location.country     = data['country']
        if "cityRank"    in data: location.cityRank    = data['cityRank']
        if "city"        in data: location.city        = data['city']
        if "stateCode"   in data: location.stateCode   = data['stateCode']
        if "stateName"   in data: location.stateName   = data['stateName']
        if "hidden"      in data: location.hidden      = data['hidden']
        if "latitude"    in data: location.latitude    = data['latitude']
        if "longitude"   in data: location.longitude   = data['longitude']
        return location


    def _parseSource(self, data):
        """ Convert the JSON-format source data into a Source object.

            'data' should be a dictionary with one or more of the following
            entries:

                "code"
                "name"
                "logo_url"
                "logo_sm_url"

            Note that this is the format received from the 3taps server after
            decoding the JSON-format data.

            We convert 'data' into a Source object, which we then return to
            the caller.
        """
        source = Source()
        if "code"        in data: source.code         = data['code']
        if "name"        in data: source.name         = data['name']
        if "logo_url"    in data: source.logoURL      = data['logo_url']
        if "logo_sm_url" in data: source.smallLogoURL = data['logo_sm_url']
        return source

