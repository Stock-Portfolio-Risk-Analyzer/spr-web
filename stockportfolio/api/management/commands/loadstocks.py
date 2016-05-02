import os

import pandas
from django.core.management.base import BaseCommand

from stockportfolio.api import utils
from stockportfolio.api.datautils.yahoo_finance import (get_company_name,
                                                        get_company_sector)
from stockportfolio.api.models import Stock
from stockportfolio.settings.base import BASE_DIR


class Command(BaseCommand):
    """
    Extends Django BaseCommand, generates all stock objects from secwiki_tickers.

    """
    help = 'Creates all of the stock objects if they do not exist'

    def handle(self, *args, **options):
        fpath = os.path.join(
            BASE_DIR, 'api', 'datautils', 'secwiki_tickers.csv')
        df = pandas.read_csv(fpath)
        for ticker in df['Ticker']:
            stock_name = get_company_name(ticker)
            stock_sector = get_company_sector(ticker)
            Stock.objects.get_or_create(
                stock_name=stock_name,
                stock_ticker=ticker,
                stock_sector=stock_sector)[0]

        self.stdout.write(
            self.style.SUCCESS('Successfully imported all stocks'))
        self.stdout.write(
            self.style.SUCCESS('Beginning price precomputing'))
        utils.precompute_prices_for_all_stocks()
        self.stdout.write(
            self.style.SUCCESS(
                'Successfully precomputed prices for all stocks'))
        self.stdout.write(
            self.style.SUCCESS('Beginning rri precomputing'))
        utils.precompute_rri_for_all_stocks()
        self.stdout.write(
            self.style.SUCCESS('Successfully precomputed RRI for all stocks'))
