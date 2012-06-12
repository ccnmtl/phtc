from pagetree_export.exportimport import import_zip
from django.core.management.base import BaseCommand
from django.conf import settings
from restclient import GET
from zipfile import ZipFile
from cStringIO import StringIO


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print "this should never be run on production"
            return
        print "fetching content from prod..."
        zc = GET(settings.PROD_BASE_URL + "_export/")
        buffer = StringIO(zc)
        zipfile = ZipFile(buffer, "r")

        import_zip(zipfile, 'main')
