import datetime

from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from stats.models import Webpage, LogFilePosition

from stats.settings import EXCLUDED_URLS

from stats import forms

class WebpageListView(LoginRequiredMixin, ListView):

    model = Webpage
    paginate_by = 10

    def get_queryset(self):
        return Webpage.objects.exclude(external_url__in=EXCLUDED_URLS). \
            order_by('-count')

@login_required
def url_view(request):

    if request.method == 'POST':
        form = forms.FilterForm(request.POST)
        if form.is_valid():
            days_back = form.cleaned_data['days_back']
            max_urls = form.cleaned_data['max_urls']
            minimum_hits = form.cleaned_data['minimum_hits']
            include_urls = form.cleaned_data['include_urls']
            if days_back:
                date_from = datetime.datetime.now() - \
                    datetime.timedelta(days=days_back)
                date_to = datetime.datetime.now()
            else:
                date_from = form.cleaned_data['date_from']
                date_to = form.cleaned_data['date_to']
        else:
            messages.add_message(request, messages.ERROR, "Please correct")
    else:
        form = forms.FilterForm()
        days_back = forms.INITIAL_DAYS_BACK
        minimum_hits = forms.INITIAL_MIN_HITS
        max_urls = forms.INITIAL_MAX_URLS
        date_from = forms.INITIAL_DATE_FROM()
        date_to = forms.INITIAL_DATE_TO()
        include_urls = ""

    webpages = Webpage.objects.exclude(external_url__in=EXCLUDED_URLS). \
        filter(created__gte=date_from).filter(created__lte=date_to). \
        filter(count__gte=minimum_hits).order_by('-count')

    if include_urls:
        include_urls = include_urls.split(" ")
        include_urls = [i.strip() for i in include_urls if i]
        webpages = webpages.filter(external_url__in=include_urls)

    if max_urls:
        webpages = webpages[:max_urls]

    total_hits = webpages.aggregate(Sum('count'))

    return render(request, "stats/webpage_list.html",
                  {
                      'webpages': webpages,
                      'total_hits': total_hits['count__sum'],
                      'form': form
                  });
