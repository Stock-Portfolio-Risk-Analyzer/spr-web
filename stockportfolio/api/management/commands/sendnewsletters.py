from django.core.management.base import BaseCommand, CommandError

from stockportfolio.api.newsletter import newsletter


class Command(BaseCommand):
    help = 'Sends a newsletter to all of the sites users'

    def handle(self, *args, **options):
        newsletter.send_emails()
        self.stdout.write(
            self.style.SUCCESS('Successfully sent out all emails!'))
