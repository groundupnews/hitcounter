import re
from urllib.parse import urlparse
from stats.models import Webpage, LogFilePosition
import datetime
from django.db import models
from django.db import transaction
from stats.settings import REGEX

def get_log_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()

    parsed_lines = parsed_lines = [re.match(REGEX, line[0:-1]).groups()
                                   for line in lines if re.match(REGEX, line[0:-1])
                                   is not None]
    return parsed_lines


def getLogFilePosition(filename):
    try:
        logfileposition = LogFilePosition.objects.get(filename=filename)
        time_accessed = logfileposition.time_accessed
        records_read = logfileposition.records_read
    except LogFilePosition.DoesNotExist:
        time_accessed = ""
        records_read = 0
    return time_accessed, records_read

def filter_log_list(log_list, time, line_num):
    if len(log_list) >= line_num:
        if log_list[line_num-1][1] == time:
            log_list = log_list[line_num:]
    result = [l for l in log_list if l[3] == '200' or l[3] == '301']
    return result

def filter_important_fields(filtered_log_list):
    return [ [l[2], l[5]] for l in filtered_log_list]

def extract_domain_from_external_url(internal_external_list):
    cleaned_list = [(r[0], urlparse(r[1]).netloc) for r in internal_external_list]
    return cleaned_list

def add_to_count(records, internal_url, external_url):
    if (internal_url, external_url) in records:
        records[(internal_url, external_url)] += 1
    else:
        try:
            webpage = Webpage.objects.get(internal_url=internal_url,
                                          external_url=external_url)
            records[(internal_url, external_url)] = webpage.count
        except Webpage.DoesNotExist:
            records[(internal_url, external_url)] = 1

def write_records(records):
    for key, value in records.items():
        try:
            webpage = Webpage.objects.get(internal_url=key[0],
                                          external_url=key[1])
        except Webpage.DoesNotExist:
            webpage = Webpage(internal_url=key[0],
                              external_url=key[1])
        webpage.count = value
        webpage.save()

def save_log_file_position(filename, time_accessed, records_read):
    try:
        logfileposition = LogFilePosition.objects.get(filename=filename)
        logfileposition.time_accessed = time_accessed
        logfileposition.records_read = records_read
    except LogFilePosition.DoesNotExist:
        logfileposition = LogFilePosition(filename=filename,
                                          time_accessed=time_accessed,
                                          records_read=records_read)
    logfileposition.save()



def process_log_file(filename):
    log_list = get_log_file(filename)
    time_accessed, records_read = getLogFilePosition(filename)
    filtered_log_list = filter_log_list(log_list, time_accessed, records_read)
    important_fields = filter_important_fields(filtered_log_list)
    cleaned_list = extract_domain_from_external_url(important_fields)
    print("A", len(cleaned_list), cleaned_list[0])
    with transaction.atomic():
        records = {}
        for item in cleaned_list:
            add_to_count(records, item[0], item[1])
        write_records(records)
        # save_log_file_position(filename, log_list[-1][1], len(log_list))
    return len(filtered_log_list)
