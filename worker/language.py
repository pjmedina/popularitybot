
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
        """Uses the Language API for senitment analysis."""
        request = self.language.documents().analyzeSentiment(
            body={
                "document": {
                    "type": "PLAIN_TEXT",
                    "language": "en",
                    "content": text
                }
            })
        response = request.execute()
        response['time_collected'] = int(time())
        return response
