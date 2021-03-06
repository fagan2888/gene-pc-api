import os
from uuid import UUID

from celery import Celery
from kombu.serialization import register
from django.conf import settings
from anyjson import loads as json_loads, dumps as json_dumps


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'generank.settings')

app = Celery('generank')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# Custom Serializer


def _loads(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return json_loads(data)


def _dumps(data):
    """ Serialize all UUID fields to a string before passing
    the rest to json.dumps.
    """
    data['args'] = [str(arg) if isinstance(arg, UUID) else arg
        for arg in data['args']]
    return json_dumps(data)


def register_uuid_json():
    """Register a encoder/decoder for UUID compatable JSON serialization."""
    register('uuid_json', _dumps, _loads,
                      content_type='application/json',
                      content_encoding='utf-8')
register_uuid_json()
