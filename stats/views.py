from django.views.generic import ListView
from django.views.generic import ListView

from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404

from django.contrib.auth.mixins import LoginRequiredMixin

from stats.models import Webpage, LogFilePosition

from stats.settings import EXCLUDED_URLS

class WebpageListView(LoginRequiredMixin, ListView):

    model = Webpage
    paginate_by = 10

    def get_queryset(self):
        return Webpage.objects.exclude(external_url__in=EXCLUDED_URLS). \
            order_by('-count')
