import pprint

from typeform.resource import Resource
from .errors import NotFoundException
from .form_response import FormResponses
from contextlib import contextmanager


@contextmanager
def non_json_client(client):

    orig_headers = client.headers
    client.headers = dict(((k,v) for (k,v) in orig_headers.items() if k != 'Content-type'))

    try:
        yield client
    finally:
        client.headers = orig_headers






class Form(Resource):
    """TypeForm Form API client"""
    model_path = 'forms'
    #
    #
    # def _request(self, method, params=None):
    #     """Helper for making API requests for this form"""
    #     path = 'form/{form_id}'.format(form_id=self.form_id)
    #     return super(Form, self)._request(method, path, params=params)

    def _get_params(self, **kwargs):
        """Helper to normalize query string parameters for our request"""
        params = dict()

        # Boolean params
        for name in ('completed',):
            value = kwargs.get(name)
            if value is not None:
                params[name] = 'true' if value else 'false'

        # Number params
        for name in ('limit', 'since', 'offset', 'until'):
            value = kwargs.get(name)
            if value is not None:
                params[name] = int(value)

        # Order by
        if 'order_by' in kwargs:
            order_by = kwargs['order_by']
            if order_by is not None:
                if ',' in order_by:
                    params['order_by[]'] = order_by
                else:
                    params['order_by'] = order_by

        # Token
        if 'token' in kwargs and kwargs['token']:
            params['token'] = kwargs['token']

        return params

    def get_responses(self, token=None, completed=None, since=None, until=None, offset=None, limit=None, order_by=None):
        """Get a list of responses for this TypeForm Form"""
        params = self._get_params(
            completed=completed,
            limit=limit,
            offset=offset,
            order_by=order_by,
            since=since,
            until=until,
            token=token,
        )

        # curl --request GET \
        # --url 'https://api.typeform.com/forms/sFAgdk/responses' \
        # --header 'authorization: bearer wJtvWMZrMRkY2Q9LEU1BFwqFp2hjpWdpRmxGNuqzveA'
        #


        path = 'forms/{form_id}/responses'.format(form_id=self.id)
        print('path:',path)
        with non_json_client(self._client) as c:
            resp = self._request('GET',path, params=params)

        return resp
        # pprint.pprint(resp)
        # return FormResponses(stats=resp.get('stats'), responses=resp.get('responses'), questions=resp.get('questions'))

    # def get_response(self, token):
    #     """Get a specific response for this TypeForm Form"""
    #     responses = self.get_responses(token=token)
    #     # Check truthy *and* length since this is a class, not a list
    #     if responses and len(responses) == 1:
    #         return responses[0]
    #
    #     raise NotFoundException('typeform client could not find response with token {token!r}'.format(token=token))

    def prepare_data_for_create(self):
        for field in self.fields:
            field.pop('id')

            choices = field.get('properties').get('choices', None)
            if choices:
                for c in choices:
                    c.pop('id')
                field['properties']['choices'] = choices

        # assert self.workspace.get()

        data = {
            'title': self.title,
            'fields': self.fields,
            'theme': self.theme,
            'hidden': getattr(self, 'hidden', [])
        }

        if self.workspace:
            data['workspace'] = self.workspace.get_api_object_ref()

        if self.thankyou_screens:
            data['thankyou_screens'] = self.thankyou_screens

        if self.welcome_screens:
            data['welcome_screens'] = self.welcome_screens

        return data

