from django.core.management.base import BaseCommand
from django.conf import settings
from pagetree.models import UserPageVisit

class Command(BaseCommand):
    args = '<userpagevisit>'
    help = 'clear out all user page visits'

    def handle(self, *args, **options):
    	UserPageVisit.objects.all().delete()
    	print "done clearing out the user page visits"