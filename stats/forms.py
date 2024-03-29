import datetime

from django import forms
from django.forms import Form


INITIAL_MAX_URLS = 100
INITIAL_MIN_HITS = 20
INITIAL_DAYS_BACK = 7

def calc_days_back():
    return datetime.datetime.now() - datetime.timedelta(days=INITIAL_DAYS_BACK)

INITIAL_DATE_FROM = calc_days_back
INITIAL_DATE_TO = datetime.datetime.now

class FilterForm(Form):
    max_urls = forms.IntegerField(initial=INITIAL_MAX_URLS,
                                      min_value=0, required=False)
    date_from = forms.DateField(initial=INITIAL_DATE_FROM())
    date_to = forms.DateField(initial=INITIAL_DATE_TO())
    minimum_hits = forms.IntegerField(initial=INITIAL_MIN_HITS,
                                      min_value=0)
    include_urls = forms.CharField(max_length=200, required=False, initial="",
                                   help_text="Separate URLs by spaces. "
                                   "Leave blank to include all.")
