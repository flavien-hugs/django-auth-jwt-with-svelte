# accounts.renderers.py


import json
from typing import Any, Mapping, Optional

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):

    charset = 'utf-8'

    def render(
        self,
        data,
        media_type: Optional[str] = None,
        renderer_context: Optional[Mapping[str, Any]] = None,
    ) -> str:

        errors = data.get('errors', None)
        token = data.get('token', None)
        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return json.dumps({'user': data})
