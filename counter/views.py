from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse

from PIL import Image

from counter.settings import RECORD_VISITS, IMAGE_FILE, IMAGE_SIZE
from counter.models import Record

image = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), (255,0,0,0))

def hit_view(request, site, slug):
    if RECORD_VISITS:
        r = Record()
        r.site = request["META.REMOTE_HOST"]
        r.url = request.path
        now = timezone.now()
        records = Record.objects.all(site=r.site,
                                     url = r.url,
                                     year = now.year,
                                     month = now.month,
                                     day = now.day,
                                     hour = now.hour)
        if len(records) == 0:
            r.save()
        else:
            r = records[0]
            r.views = r.views + 1
            r.save()

    if IMAGE_FILE:
        with open(IMAGE_FILE, "rb") as f:
            response = HttpResponse(f.read(), content_type="image/jpeg")
    else:
        response = HttpResponse(content_type="image/jpeg")
        image.save(response, "JPEG")

    return response
