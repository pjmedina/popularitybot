
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

    def detect_sentiment(self, text: str, max_results=10, num_retries=0):
        """Uses the Language API for senitment analysis."""
        if text is None:
            raise ValueError("Text is None")
        if text == "":
            return None
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

    @staticmethod
    def get_score_and_magnitude(response):
        if 'documentSentiment' in response:
            document_sentiment = response['documentSentiment']
            if 'score' in document_sentiment and 'magnitude' in document_sentiment:
                return response['documentSentiment']['score'], response['documentSentiment']['magnitude']
            else:
                raise ValueError("Score or magnitude are not in response.")
        else:
            raise ValueError("Document sentiment not in response.")

    def get_result_for_storage(self, reddit_post_id, post_title, post_content):
        response = {}
        post_title_sentiment_response = self.detect_sentiment(post_title)
        post_title_score, post_title_magnitude = LanguageApi.get_score_and_magnitude(post_title_sentiment_response)
        post_content_score, post_content_magnitude = None, None
        if post_content is not None:
            post_content_sentiment_response = self.detect_sentiment(post_content)
            post_content_score, post_content_magnitude = LanguageApi.get_score_and_magnitude(post_content_sentiment_response)
        response['_id'] = reddit_post_id
        response['title_score'] = post_title_score
        response['title_magnitude'] = post_title_magnitude
        response['content_score'] = post_content_score
        response['content_magnitude'] = post_content_magnitude
        return response
