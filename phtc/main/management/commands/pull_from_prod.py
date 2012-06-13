from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.simplejson import loads
from pagetree.models import Hierarchy
from restclient import GET


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print "this should never be run on production"
            return
        print "fetching content from prod..."
        d = loads(GET(settings.PROD_BASE_URL + "_export/"))
        print str(d)
        print "removing old pagetree hierarchy"
        Hierarchy.objects.all().delete()
        print "importing the new one"
        Hierarchy.from_dict(d)
        print "done"
