import requests

from .compat import urlparse
from .errors import (NotAuthorizedException, NotFoundException, InvalidRequestException,
                     RateLimitException, UnknownException)
import json
import pprint


class Client(object):
    """TypeForm API client"""
    BASE_URL = 'https://api.typeform.com'
    api_key = None

    def __init__(self):
        """Constructor for TypeForm API client"""
        super(Client, self).__init__()

        assert self.api_key, 'Set API_KEY use {}.config(api_key) '.format(self.__class__.__name__)

        # self.api_key = api_key
        self._client = requests.Session()
        self._client.headers = {
            'User-Agent': 'python-typeform/0.1.1',
            'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.api_key)
        }

    @classmethod
    def config(cls, api_key):
        Client.api_key = api_key

    def _request(self, method, path, params=None, data=None):
        """Helper method to make requests to the TypeForm API"""
        # Append our API key on to the request params
        if params is None:
            params = dict()

        # Prepare data for post
        if data and method.upper() == 'POST':
            data = json.dumps(data)

        # Get our full request URI, e.g. `form/abc123` -> `https://api.typeform.com/v1/form/abc123`
        url = urlparse.urljoin(self.BASE_URL, path)

        # Make our API request
        resp = self._client.request(method=method, url=url, params=params, data=data)

        # On 500 error we don't get JSON, so no reason to even try
        if resp.status_code == 500:
            raise UnknownException('typeform client received 500 response from api')

        # On delete object
        if resp.status_code == 204:
            return True

        # Status code 400 not have json data
        if resp.status_code == 400:
            raise UnknownException('Error(400) {}'.format(resp.text))

        # Attempt to decode our JSON
        # DEV: In every case (other than 500) we have gotten JSON back, but catch exception just in case
        try:
            data = resp.json()
        except ValueError:
            raise UnknownException('typeform client could not decode json from response')

        # Good response, just return it
        if resp.status_code in [200, 201]:
            return data

        # Api Errors
        # Handle any exceptions
        message = data.get('message')
        if resp.status_code == 404:
            raise NotFoundException(message)
        elif resp.status_code == 403:
            raise NotAuthorizedException(message)
        elif resp.status_code == 400:
            raise InvalidRequestException(message)
        elif resp.status_code == 429:
            raise RateLimitException(message)

        # Hmm, not sure how we got here, just raise hell
        raise UnknownException(
            'typeform client received unknown response status code {code!r}'.format(code=resp.status_code)
        )
