""" threetaps.api.clients.postingAPIClient

    This Python module implements the 3taps Posting API client object.
"""
from threetaps.api.base   import APIClient
from threetaps.api.models import Posting

import simplejson as json

#############################################################################

class PostingAPIClient(APIClient):
    """ A client for the 3taps Posting API.
    """
    def get(self, postKey):
        """ Retrieve a posting with the given postKey.

            'postKey' should be the posting key for a desired posting.

            We attempt to retrieve the given posting from the 3taps system.
            Upon completion, we return a dictionary with the following entries:

                'success'

                    If the posting was found, this will be set to True.

                'posting'

                    The Posting object which was retrieved (success=True).

                'error'

                    If a problem occurred (success=False), this will be a
                    dictionary with 'code' and 'message' entries describing the
                    error that occurred.

            Note that if the 3taps server cannot be contacted for some reason,
            we return None.
        """
        response = self.sendRequest("posting/get/" + postKey)

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])
        if "code" in results and "message" in results:
            # We received an error object rather than the desired posting ->
            # the posting doesn't exist.
            return {'success' : False,
                    'error'   : {'code'    : int(results['code']),
                                 'message' : results['message']}}

        return {'success' : True,
                'posting' : Posting(**results)}


    def create(self, posting):
        """ Create a new posting in the 3taps system.

            'posting' should be a Posting object representing the posting to
            create.  Note that the posting should not include a 'postKey'
            entry, as this will be allocated by the 3taps system.

            We attempt to insert the new posting into the 3taps system.  Upon
            completion, we return a dictionary with the following entries:

                'postKey'

                    The newly-allocated posting key for this posting.

                'error'

                    If a problem occurred with the posting, this will be a
                    dictionary with 'code' and 'message' entries describing the
                    error that occurred.  If there was no error, there won't be
                    an "error" entry in the response dictionary.

            Note that if the 3taps server cannot be contacted for some reason,
            we return None.
        """
        response = self.createMany([posting])
        if response != None:
            return response[0]
        else:
            return None


    def createMany(self, postings):
        """ Create multiple new postings in the 3taps system.

            'postings' should be a list of Posting objects representing the
            postings to create.  Note that the postings should not include a
            'postKey' entry, as this will be allocated by the 3taps system.

            We attempt to insert the new postings into the 3taps system.  Upon
            completion, we return a list of responses, one for each posting in
            the 'postings' list.  Each response will be a dictionary with the
            following entries:

                'postKey'

                    The newly-allocated posting key for this posting.

                'error'

                    If a problem occurred with the posting, this will be a
                    dictionary with 'code' and 'message' entries describing the
                    error that occurred.  If there was no error, there won't be
                    an "error" entry in the response dictionary.

            Note that if the 3taps server cannot be contacted for some reason,
            we return None.
        """
        postingDicts = []
        for posting in postings:
            postingDicts.append(self._postingToDict(posting))

        postingData = json.dumps(postingDicts)

        response = self.sendRequest("posting/create", "POST",
                                    postings=postingData)

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])
        return results


    def update(self, posting):
        """ Update the contents of a posting in the 3taps system.

            'posting' should be a Posting object, which includes the posting
            key of the posting to update.  Any other attributes set in the
            Posting object will be used to override the existing value in the
            3taps database.

            Upon completion, we return True if and only if the update request
            was successful.
        """
        return self.updateMany([posting])


    def updateMany(self, postings):
        """ Update the contents of multiple postings in the 3taps system.

            'postings' should be a list of Posting objects, where each Posting
            object includes the posting key of the posting to update.  Any
            other attributes set in the Posting object will be used to override
            the existing value in the 3taps database.

            Upon completion, we return True if and only if the update request
            was successful.
        """
        updates = []
        for posting in postings:
            postingDict = self._postingToDict(posting)
            if 'postKey' in postingDict:
                postKey = postingDict['postKey']
                del postingDict['postKey']
                updates.append((postKey, postingDict))

        data = json.dumps(updates)

        response = self.sendRequest("posting/update", "POST",
                                    data=data)

        if (response == None) or (response['status'] != 200):
            return False # An error occurred.

        results = json.loads(response['contents'])
        return results['success']


    def delete(self, postKey):
        """ Delete the posting with the given post key from the 3taps system.

            We ask the 3taps server to delete the given posting.  Upon
            completion, we return True if and only if the posting was
            successfully deleted.
        """
        return self.deleteMany([postKey])


    def deleteMany(self, postKeys):
        """ Delete multiple postings from the 3taps system.

            'postKeys' should be a list of posting keys to delete.  Upon
            completion, we return True if and only if all the postings were
            successfully deleted.
        """
        data = json.dumps(postKeys)

        response = self.sendRequest("posting/delete", "POST",
                                    data=data)

        if (response == None) or (response['status'] != 200):
            return False # An error occurred.

        results = json.loads(response['contents'])
        return results['success']

    # =====================
    # == PRIVATE METHODS ==
    # =====================

    def _postingToDict(self, posting):
        """ Convert a Posting object to a dictionary.

            We create a dictionary with key/value entries matching the contents
            of the given Posting object.
        """
        postDict = {}
        if posting.postKey != None:
            postDict['postKey'] = posting.postKey
        if posting.location != None:
            postDict['location'] = posting.location
        if posting.category != None:
            postDict['category'] = posting.category
        if posting.source != None:
            postDict['source'] = posting.source
        if posting.heading != None:
            postDict['heading'] = posting.heading
        if posting.body != None:
            postDict['body'] = posting.body
        if posting.latitude != None:
            postDict['latitude'] = posting.latitude
        if posting.longitude != None:
            postDict['longitude'] = posting.longitude
        if posting.language != None:
            postDict['language'] = posting.language
        if posting.price != None:
            postDict['price'] = posting.price
        if posting.currency != None:
            postDict['currency'] = posting.currency
        if posting.images != None and len(posting.images) > 0:
            postDict['images'] = posting.images
        if posting.externalID != None:
            postDict['externalID'] = posting.externalID
        if posting.externalURL != None:
            postDict['externalURL'] = posting.externalURL
        if posting.accountName != None:
            postDict['accountName'] = posting.accountName
        if posting.accountID != None:
            postDict['accountID'] = posting.accountID
        if posting.timestamp != None:
            postDict['timestamp'] = \
                posting.timestamp.strftime("%Y/%m/%d %H:%M:%S UTC")
        if posting.expiration != None:
            postDict['expiration'] = \
                posting.expiration.strftime("%Y/%m/%d %H:%M:%S UTC")
        if posting.annotations != None and len(posting.annotations) > 0:
            postDict['annotations'] = posting.annotations
        if posting.trustedAnnotations != None \
           and len(posting.trustedAnnotations) > 0:
            postDict['trustedAnnotations'] = posting.trustedAnnotations
        if posting.clickCount != None:
            postDict['clickCount'] = posting.clickCount
        return postDict

