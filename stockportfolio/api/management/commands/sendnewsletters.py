from django.core.management.base import BaseCommand

from stockportfolio.api.newsletter import newsletter


class Command(BaseCommand):
    """
    Extends Django BaseCommand, executes the send_emails funciton.
    All users will be sent a newsletter with information on their
    default portfolio.

    """
    help = 'Sends a newsletter to all of the sites users'

    def handle(self, *args, **options):
        """
        Function sends an email to all users with info on their portfolio.
        Sends a successful message.

        :param args: None
        :param options: None
        :return: None
        """
        newsletter.send_emails()
        self.stdout.write(
            self.style.SUCCESS('Successfully sent out all emails!'))
