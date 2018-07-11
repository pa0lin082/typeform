from .errors import NotFoundException
from typeform.resource import Resource
import pprint




class Workspace(Resource):
    """TypeWorkspace Workspace API client"""
    model_path = 'workspaces'

    def prepare_data_for_create(self):
        data = {
            'name': self.name
        }
        return data
