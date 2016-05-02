from django.core.management.base import BaseCommand

from stockportfolio.api import utils as utils


class Command(BaseCommand):
    """
    Extends Django BaseCommand, generates all Risk Values for all portfolios
    in Database.

    """
    help = 'calculates the current RRI for all portfolios'

    def handle(self, *args, **options):
        """
        Function loads all risk values for portfolio in Database

        :param args: None
        :param options: None
        :return: None
        """
        utils.update_value_for_all_portfolios()
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully updated values for all portfolios'))
        utils.update_rri_for_all_portfolios()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated RRI for all portfolios'))
        utils.update_rank_for_all_portfolios()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated rank for all portfolios'))
        utils.update_rri_for_all_stocks()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated RRI for all stocks'))
        utils.update_price_for_all_stocks()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated prices for all stocks'))
