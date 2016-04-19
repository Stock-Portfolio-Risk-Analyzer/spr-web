from django.core.management.base import BaseCommand, CommandError
from stockportfolio.api import utils as utils


class Command(BaseCommand):
    help = 'calculates the current RRI for all portfolios'

    def handle(self, *args, **options):
        utils.precompute_prices_for_all_stocks()
        self.stdout.write(
            self.style.SUCCESS('Successfully precomputed prices for all stocks'))
        utils.precompute_rri_for_all_stocks()
        self.stdout.write(
            self.style.SUCCESS('Successfully precomputed RRI for all stocks'))
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
