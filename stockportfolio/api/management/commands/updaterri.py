from django.core.management.base import BaseCommand, CommandError
from stockportfolio.api.utils import update_rri_for_all_portfolios, update_rank_for_all_portfolios


class Command(BaseCommand):
    help = 'calculates the current RRI for all portfolios'

    def handle(self, *args, **options):
        update_rri_for_all_portfolios()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated RRI for all portfolios'))
        update_rank_for_all_portfolios()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated rank for all portfolios'))
