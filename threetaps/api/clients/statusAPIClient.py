""" threetaps.api.clients.statusAPIClient

    This Python module implements the 3taps Status API client object.
"""
from threetaps.api.base import APIClient

import datetime
import simplejson as json

#############################################################################

class StatusAPIClient(APIClient):
    """ A client for the 3taps Status API.
    """
    def update(self, events):
        """ Send a status update to the 3taps server.

            'events' should be a list of status events, where each list item is
            a dictionary with the following entries:

                'status'

                    The event's status.  The following event status values are
                    currently supported:

                        "found"
                        "got"
                        "processed"
                        "sent"
                        "received"
                        "indexed"

                'externalID'

                    The external ID for this posting in the source system.

                'source'

                    The 5-character source code for this posting.

                'timestamp'

                    An optional datetime.datetime object representing the date
                    and time that this status update occurred, in UTC.  If this
                    is not present, the timestamp will default to "now".

                'attributes'

                    An optional dictionary mapping attribute names to their
                    values for additional information to store about this
                    event.

            Upon completion, we return a dictionary with the following entries:

                'success'

                    This will be set to True if and only if the status update
                    succeeded.

                'error'

                    If the status update failed, this will be a dictionary with
                    'code' and 'message' entries describing the error that
                    occurred.

            Note that if the 3taps server cannot be contacted for some reason,
            we return None.
        """
        eventData = []
        for event in events:
            data = {}
            data['status']     = event['status']
            data['externalID'] = event['externalID']
            data['source']     = event['source']
            if "timestamp" in event:
                data['timestamp']  = \
                        event['timestamp'].strftime("%Y/%m/%d %H:%M:%S UTC")
            if "attributes" in event:
                data['attributes'] = event['attributes']
            eventData.append(data)

        response = self.sendRequest("status/update", "POST",
                                    events=json.dumps(eventData))

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])

        if results['code'] == 200: # HTTP "OK" status value.
            return {'success' : True}
        else:
            return {'success' : False,
                    'error'   : results}


    def get(self, postings):
        """ Return the status history for one or more postings.

            'postings' should be a list of postings to retrieve the status
            history for, where each item in this list is a Posting object with
            just two fields filled in:

                externalID
                source

            Upon completion, we return a list of status histories, one for each
            posting.  Each item in the returned list will be a dictionary with
            the following entries:

                'exists'

                    This will be set to True if and only if the Status API has
                    history information for the given posting.

                'externalID'

                    A copy of the external ID for this posting, copied from the
                    Posting object.

                'source'

                    A copy of the source for this posting, copied from the
                    Posting object.

                'history'

                    A dictionary mapping status values ("found", "got",
                    "processed", etc) to a list of updates received for that
                    posting and status.  Each item in the list of updates will
                    itself be a dictionary with the following entries:

                        'timestamp'

                            A datetime.datetime() object representing the date
                            and time at which this update occurred, in UTC.

                        'errors'

                            A list of errors which have occurred while updating
                            this posting's status.  Each item in this list wil
                            be a dictionary with 'code' and 'message' entries.

                        'attributes'

                            A dictionary mapping attribute names to values,
                            reflecting the attribute values that were passed to
                            the update() API call.

            Note that if the 3taps server cannot be contacted for some reason,
            we return None.
        """
        postingData = []
        for posting in postings:
            postingData.append({'externalID' : posting.externalID,
                                'source'     : posting.source})

        response = self.sendRequest("status/get", "POST",
                                    postings=json.dumps(postingData))

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])

        histories = []
        for entry in results:
            history = {}
            history['exists']     = entry['exists']
            history['externalID'] = entry['externalID']
            history['source']     = entry['source']
            history['history']    = {}

            for status,statusUpdates in entry['history'].items():
                history['history'][status] = []
                for statusUpdate in statusUpdates:
                    update = {}
                    update['timestamp'] = \
                        datetime.datetime.strptime(statusUpdate['timestamp'],
                                                   "%Y/%m/%d %H:%M:%S %Z")
                    update['errors']     = statusUpdate.get("errors",     [])
                    update['attributes'] = statusUpdate.get("attributes", {})
                    history['history'][status].append(update)

            histories.append(history)

        return histories


    def system(self):
        """ Return the current status of the 3taps system.

            Upon completion, we return a dictionary with the following entries:

                'code'

                    The 3taps status code value reflecting the current system
                    status.

                'message'

                    A string describing the current status in a human-readable
                    form.

            Note that if the 3taps server cannot be contacted for some reason,
            we return None.
        """
        response = self.sendRequest("status/system")

        if (response == None) or (response['status'] != 200):
            return None # An error occurred.

        results = json.loads(response['contents'])
        return results

