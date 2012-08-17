from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    args = '<hierarchy name> (optional)'
    help = 'clear out all user page visits'

    def handle(self, *args, **options):
    	print "done clearing out the user page visits"