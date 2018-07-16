import pprint

from typeform.resource import Resource
from .errors import NotFoundException
from .form_response import FormResponses


class Form(Resource):
    """TypeForm Form API client"""
    model_path = 'forms'
    #
    #
    # def _get_params(self, **kwargs):
    #     """Helper to normalize query string parameters for our request"""
    #     params = dict()
    #
    #     # Boolean params
    #     for name in ('completed',):
    #         value = kwargs.get(name)
    #         if value is not None:
    #             params[name] = 'true' if value else 'false'
    #
    #     # Number params
    #     for name in ('limit', 'since', 'offset', 'until'):
    #         value = kwargs.get(name)
    #         if value is not None:
    #             params[name] = int(value)
    #
    #     # Order by
    #     if 'order_by' in kwargs:
    #         order_by = kwargs['order_by']
    #         if order_by is not None:
    #             if ',' in order_by:
    #                 params['order_by[]'] = order_by
    #             else:
    #                 params['order_by'] = order_by
    #
    #     # Token
    #     if 'token' in kwargs:
    #         params['token'] = kwargs['token']
    #
    #     return params
    #
    # def get_responses(self, token=None, completed=None, since=None, until=None, offset=None, limit=None, order_by=None):
    #     """Get a list of responses for this TypeForm Form"""
    #     params = self._get_params(
    #         completed=completed,
    #         limit=limit,
    #         offset=offset,
    #         order_by=order_by,
    #         since=since,
    #         until=until,
    #         token=token,
    #     )
    #
    #     resp = self._request('GET', params=params)
    #     pprint.pprint(resp)
    #     return FormResponses(stats=resp.get('stats'), responses=resp.get('responses'), questions=resp.get('questions'))
    #
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
            'hidden': getattr(self, 'hidden', []),
            'workspace': self.workspace.get_api_object_ref()
        }
        return data

