from django.conf import settings

RECORD_VISITS = getattr(settings, 'COUNTER_RECORD_VISITS', False)
IMAGE_FILE = getattr(settings, 'COUNTER_IMAGE_FILE', None)
