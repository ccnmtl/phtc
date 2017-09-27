from django.core.management.base import BaseCommand
from optparse import make_option
from django.contrib.auth.models import User
from pagetree.models import UserPageVisit


class Command(BaseCommand):
    args = '<username>'
    help = 'clear out all user page visits'

    option_list = BaseCommand.option_list + (
        make_option('--username',
                    action='store',
                    type='string',
                    default=False,
                    help='Delete specific user history'),
    )

    def handle(self, *args, **options):
        if options['username']:
            username = options['username']
            try:
                user = User.objects.get(username__exact=username)
                upv = UserPageVisit.objects.filter(user_id=user.id)
                for v in upv:
                    v.delete()
            except User.DoesNotExist:
                pass
            print "done clearing out " + username + "\'s user page visits"
        else:
            UserPageVisit.objects.all().delete()
            print "done clearing out all user page visits"
