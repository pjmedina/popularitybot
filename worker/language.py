
import os
from time import time

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


class LanguageApi(object):
    def __init__(self, google_application_credentials_path="client-secret.json"):
        if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') != 'True':
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_application_credentials_path
        self.language = self._create_client()

    def _create_client(self):
        credentials = GoogleCredentials.get_application_default()
        return discovery.build(
            'language', 'v1beta2', credentials=credentials,
            discoveryServiceUrl=DISCOVERY_URL)

    def detect_sentiment(self, text, max_results=10, num_retries=0):
        """Uses the Vision API for label detection,
        text detection, web detection, and image properties.
        """
        merged_response = None
        split_text = self.split(text, 16)
        for itext in split_text:
            batch_request = []

            for text in itext:
                batch_request.append({
                    {
                        "document": {
                          "type": "PLAIN_TEXT",
                          "language": "en",
                          "content": text
                        },
                        "encodingType": "UTF32",
                    }
                })
            request = self.language.documents().analyzeSentiment(
                body={'requests': batch_request})

            response = request.execute()

            time_collected = int(time())
            # we don't need the bounding blocks, which take up a ton of space
            try:
                res = response.get('responses', [])
                for r in res:
                    r['time_collected'] = time_collected
            except KeyError:
                print("Key doesn't exist")
            if merged_response is None:
                merged_response = response
            else:
                merged_res = merged_response.get('responses')
                for res_item in response.get('responses'):
                    merged_res.append(res_item)
        return merged_response

    def split(self, arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr = arr[size:]
        arrs.append(arr)
        return arrs
