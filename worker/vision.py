# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import os
import logging
import json
from time import time

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


class VisionApi(object):
    def __init__(self, google_application_credentials_path="client-secret.json"):
        if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') != 'True':
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_application_credentials_path
        self.vision = self._create_client()

    def _create_client(self):
        credentials = GoogleCredentials.get_application_default()
        return discovery.build(
            'vision', 'v1', credentials=credentials,
            discoveryServiceUrl=DISCOVERY_URL)

    def detect_images_info(self, image_urls, max_results=10, num_retries=0):
        """Uses the Vision API for label detection,
        text detection, web detection, and image properties.
        """
        merged_response = None
        split_image_urls = self.split(image_urls, 16)
        for iurls in split_image_urls:
            batch_request = []

            for image_url in iurls:
                batch_request.append({
                    'image': {
                        'source': {
                            'imageUri': image_url
                        }
                    },
                    'features': [
                        {
                            'type': 'LABEL_DETECTION',
                            'maxResults': max_results
                        },
                        {
                            'type': 'TEXT_DETECTION'
                        },
                        {
                            'type': 'WEB_DETECTION'
                        },
                        {
                            'type': 'IMAGE_PROPERTIES',
                        }
                    ]
                })

            request = self.vision.images().annotate(
                body={'requests': batch_request})

            response = request.execute(num_retries=num_retries)

            time_collected = int(time())
            # we don't need the bounding blocks, which take up a ton of space
            try:
                res = response.get('responses', [])
                for r in res:
                    r['time_collected'] = time_collected
                    ft = r.get('fullTextAnnotation')
                    if ft is not None:
                        for page in ft.get('pages'):
                            if page is not None:
                                del page['blocks']
                    else:
                        logging.info("Did not have fullTextAnnotation: {}".format(r))
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
