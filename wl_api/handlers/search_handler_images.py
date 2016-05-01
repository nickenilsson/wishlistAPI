from wl_api.handlers.base import BaseHandler
import tornado
import requests
import urllib
import json

class SearchImagesHandler(BaseHandler):

    GOOGLE_API_KEY = 'AIzaSyBdV1Emfi7Zd-T8_PQ1tr_Av7G4WuGpHOo'
    API_ID = '012147580588716782987:8xdixcfdasg'
    FIELDS = 'items(pagemap/cse_image)'
    GOOGLE_SEARCH_URL_TEMPLATE = 'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={api_id}&q={query}&fields={fields}'

    @tornado.web.authenticated
    def get(self):
        query = urllib.quote(self.get_argument('q'))
        search_url = self.GOOGLE_SEARCH_URL_TEMPLATE.format(api_key=self.GOOGLE_API_KEY, api_id=self.API_ID, query=query)

        response = requests.get(search_url)
        response.raise_for_status()
        response_dict = json.loads(response.text)

        self.write({'response': response_dict['items']})
        self.finish()


