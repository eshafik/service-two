import logging
from typing import Union

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError
from apps.user.models import User

logger = logging.getLogger('django')


def authentication(token: str) -> Union[User, object]:
    url = f'{settings.AUTH_HOST}/api/v1.0/system/users/decode-token'
    try:
        resp = requests.get(url=url, headers={'Authorization': token}, timeout=settings.REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            return User(**data['data'])
        return
    except (requests.ReadTimeout, requests.Timeout) as err:
        logger.error(f'error response from auth. {err}')
        return
