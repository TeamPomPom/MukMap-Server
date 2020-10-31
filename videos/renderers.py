from rest_framework.renderers import BaseRenderer
from rest_framework.utils import json


class QuerySearchResultRenderer(BaseRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            "videos": [],
            "channel": {},
        }
        if data.get("videos"):
            response_dict["videos"] = data.get("videos")
        if data.get("channel"):
            response_dict["channel"] = data.get("channel")
        data = response_dict
        return json.dumps(data)
