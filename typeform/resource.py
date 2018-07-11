import pprint

from typeform.client import Client



class ResourceNotFound(Exception):
    pass

class MultipleResourcesFound(Exception):
    pass


class Resource(Client):
    model_path = None

    def __init__(self, id=None, *args, **kwargs):
        """Constructor for TypeForm Resource API client"""

        assert self.model_path, 'self.model_path is not setted for {}'.format(self.__class__.__name__)

        self.id = id
        self.populate_from_api(kwargs)
        super(Resource, self).__init__()

    def populate_from_api(self, *args, **kwargs):

        for k, value in kwargs.items():
            setattr(self, k, value)

        self.api_data = kwargs

        # raise NotImplementedError()

    def get_api_object_ref(self):
        return {
            'href': self.href
        }

    @classmethod
    def get(cls, id):
        return cls(id).retrieve()

    @classmethod
    def search_one(cls, term):
        results = cls.search(term)
        if results.get('total_items', 0) == 0:
            return None
        elif results.get('total_items', 0) == 1:
            return results.get('items')[0]
        else:
            raise MultipleResourcesFound()


    @classmethod
    def search(cls, term):

        return cls.all(search_term=term)


    @classmethod
    def all(cls, search_term=None):

        params =  dict()
        if search_term:
            params['search'] = search_term

        path = '{}'.format(cls.model_path)
        resp = cls()._request('GET', path, params=params)

        items = resp.get('items')
        for i in items:
            i['href'] = i.pop('self').get('href')

        resp.update({
            'items': [cls(**item) for item in items]
        })

        return resp

    @classmethod
    def create(cls, **kwargs):
        new_instance = cls()
        new_instance.populate_from_api(**kwargs)
        return new_instance.save()

    def list(self):
        return []

    def retrieve(self):
        path = '{model}/{id}'.format(model=self.model_path, id=self.id)
        resp = self._request('GET', path)

        if 'self' in resp:
            resp['href'] = resp.pop('self').get('href')

        self.populate_from_api(**resp)
        return self

    def delete(self):
        path = '{model}/{id}'.format(model=self.model_path, id=self.id)
        resp = self._request('DELETE', path)
        del self
        return True


    def save(self):
        if self.id:
            return self._update()
        else:
            return self._create()

    def _update(self):
        pass

    def prepare_data_for_create(self):
        raise NotImplementedError

    def _create(self):

        data = self.prepare_data_for_create()

        path = '{}'.format(self.model_path)
        resp = self._request('POST', path, data=data)
        if 'self' in resp:
            resp['href'] = resp.pop('self').get('href')

        self.populate_from_api(**resp)

        return self

    def __repr__(self):
        return '{class_name!r}(api_key={api_key!r}, id={id!r})'.format(class_name=self.__class__.__name__,
                                                                       api_key=self.api_key, id=self.id)
