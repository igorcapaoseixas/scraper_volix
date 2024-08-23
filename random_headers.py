import random
import logging

class RandomHeaders:
    
    def __init__(self, scrapeops_key, http_client):
        self.scrapeops_key = scrapeops_key
        self.http_client = http_client  
        self.url = f'http://headers.scrapeops.io/v1/browser-headers?api_key={self.scrapeops_key}'
        self.header_list = []
        self.logger = logging.getLogger(__name__)


    def get_headers_list(self):
        try:
            response = self.http_client.get(self.url)
            response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
            json_response = response.json()
            self.header_list = json_response.get('result', [])
            self.logger.info("Headers list retrieved successfully.")
        except Exception as e:
            self.logger.error(f"Error retrieving headers: {e}")
            self.header_list = []
        return self.header_list


    def get_random_header(self, header_list):
        if not header_list:
            self.logger.warning("Header list is empty, fetching new headers.")
            self.get_headers_list()
        
        if header_list:
            random_header = random.choice(header_list)
            self.logger.info(f'Your random_header is {random_header}')
            return random_header
        else:
            self.logger.error("No headers available to choose from.")
            return None