from django.core.management.base import BaseCommand, CommandError
from stats.utils import process_log_file

class Command(BaseCommand):
    help = 'Reads log file and counts hits to webpages'

    def add_arguments(self, parser):
        parser.add_argument('logfile', type=str)

    def handle(self, *args, **options):
        #try:
        lines_processed = process_log_file(options['logfile'])
        print("Successfully processed " +str(lines_processed))
        #except Exception as e:
        # print("Failure processing log file " + str(e))
