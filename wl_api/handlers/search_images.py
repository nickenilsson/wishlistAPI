from wl_api.handlers.base import BaseHandler
import tornado
import requests
import urllib
import json
from wl_api.models import Image


class SearchImagesHandler(BaseHandler):

    GOOGLE_API_KEY = 'AIzaSyBdV1Emfi7Zd-T8_PQ1tr_Av7G4WuGpHOo'
    API_ID = '012147580588716782987:8xdixcfdasg'
    FIELDS = 'items(pagemap/cse_image)'
    GOOGLE_SEARCH_URL_TEMPLATE = 'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={api_id}&q={query}&fields={fields}&searchType=image'

    @tornado.web.authenticated
    def get(self):
        try:
            query = urllib.quote(self.get_argument('q'))
            size = int(self.get_argument('size', 5))
        except Exception, e:
            raise tornado.web.HTTPError(400, 'Invalid or missing parameters')

        search_url = self.GOOGLE_SEARCH_URL_TEMPLATE.format(
                        api_key=self.GOOGLE_API_KEY,
                        api_id=self.API_ID,
                        query=query,
                        fields= self.FIELDS
        )

        response = requests.get(search_url)
        response.raise_for_status()
        response_dict = json.loads(response.text)

        images = [Image(url=r['pagemap']['cse_image'][0]['src']).store for r in response_dict['items']]
        self.write({'response': {'images':images}})
        self.finish()


