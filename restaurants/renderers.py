from rest_framework.renderers import BaseRenderer
from rest_framework.utils import json


class QuerySearchResultRenderer(BaseRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            "restaurants": [],
            "channel": {},
        }
        if data.get("restaurants"):
            response_dict["restaurants"] = data.get("restaurants")
        if data.get("channel"):
            response_dict["channel"] = data.get("channel")
        data = response_dict
        return json.dumps(data)
