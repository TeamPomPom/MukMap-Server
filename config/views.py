from rest_framework.viewsets import ModelViewSet
from rest_framework_api_key.permissions import HasAPIKey


class APIKeyModelViewSet(ModelViewSet):
    def get_base_permission(self):
        return [HasAPIKey]
