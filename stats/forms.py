import datetime

from django import forms
from django.forms import Form


INITIAL_MAX_URLS = 100
INITIAL_DAYS_BACK = 7

def calc_days_back():
    return datetime.datetime.now() - datetime.timedelta(days=INITIAL_DAYS_BACK)

INITIAL_DATE_FROM = calc_days_back
INITIAL_DATE_TO = datetime.datetime.now

class FilterForm(Form):
    max_urls = forms.IntegerField(initial=INITIAL_MAX_URLS,
                                  min_value=0, required=False)
    days_back = forms.IntegerField(initial=INITIAL_DAYS_BACK,
                                   min_value=0, required=False,
                                   help_text="Unless this is zero, it takes"
                                   " priority over Date from and Date to.")
    date_from = forms.DateField(initial=INITIAL_DATE_FROM())
    date_to = forms.DateField(initial=INITIAL_DATE_TO())
