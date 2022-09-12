import base64
import re
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers


class Base64ImageField(serializers.Field):

    def to_internal_value(self, data):
        data = re.split(';|,', data)
        image_string = data.pop()
        encoding = data.pop()
        ext = data.pop().split('/')[-1]
        if encoding == 'base64':
            path = f'{str(uuid.uuid4())}.{ext}'
            image = base64.b64decode(image_string)
            data = ContentFile(image)
            default_storage.save(path, data)
            return path
        raise serializers.ValidationError(f'Wrong image encoding {encoding}')
