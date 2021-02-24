from django.conf import settings

REGEX = getattr(settings, "STATS_REGEX",
            '([(\\d\\.)]+) - - \\[(.*?)\\] "(.*?)" (\\d+) (\\d+) "(.*?)" "(.*?)"')

EXCLUDED_URLS = getattr(settings, "STATS_EXCLUDED_URLS",[])
