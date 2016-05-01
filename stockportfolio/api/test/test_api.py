import json

from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import RequestFactory, TestCase

from stockportfolio.api import api
from stockportfolio.api.models import Portfolio


class ApiTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='testing123')
        self.portfolio = Portfolio.objects.create(portfolio_user=self.user)
        self.portfolio.save()

    def test_add_stock(self):

        url = "%s?stock=AAPL&quantity=10"
        request = self.factory.get(
            url % reverse(
                'add_stock',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = self.user
        response = api.add_stock(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            reverse(
                'get_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = self.user
        response = api.get_portfolio(
            request, portfolio_id=self.portfolio.portfolio_id)
        portfolio = json.loads(response.content)
        aapl = portfolio['stocks'][0]
        expected_aapl = {'sector': 'Consumer Goods', 'name': 'Apple Inc.',
                         'price': 105.93, 'mkt_value': 1059.3,
                         'ticker': 'AAPL', 'quantity': 10}
        expected_aapl.pop('price', None)
        expected_aapl.pop('mkt_value', None)
        aapl.pop('price', None)
        aapl.pop('mkt_value', None)
        for key in aapl.keys():
            self.assertAlmostEqual(aapl[key], expected_aapl[key])

    def test_remove_stock(self):

        # add the stock
        url = "%s?stock=AAPL&quantity=10"
        request = self.factory.get(
            url % reverse(
                'add_stock',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = self.user
        response = api.add_stock(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 200)

        # remove the stock
        url = '%s?stock=AAPL'
        request = self.factory.get(
            url % reverse(
                'remove_stock',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = self.user
        response = api.remove_stock(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 200)

        # check the portfolio
        request = self.factory.get(
            reverse(
                'get_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = self.user
        response = api.get_portfolio(
            request, portfolio_id=self.portfolio.portfolio_id)
        portfolio = json.loads(response.content)
        self.assertEqual(len(portfolio['stocks']), 0)

    def test_create_portfolio(self):
        request = self.factory.get(
            reverse('create_portfolio', kwargs={'user_id': self.user.id})
        )
        request.user = self.user
        response = api.create_portfolio(request, user_id=self.user.id)
        self.assertEqual(response.status_code, 200)

        # get the portfolio
        request = self.factory.get(
            reverse('get_portfolio_by_user', kwargs={'user_id': self.user.id})
        )
        request.user = self.user
        response = api.get_portfolio_by_user(request, user_id=self.user.id)
        self.assertEqual(response.status_code, 200)
        portfolio = json.loads(response.content)
        expected_content = json.loads(
            '{"risk_history": [], "portfolio_id": 2, "sector_allocations": {},'
            '"date_created": "2016-03-17 02:35:55.273000", "stocks": [], '
            '"name": null, "rank": null}')
        portfolio.pop('date_created', None)
        expected_content.update(
            {'portfolio_userid': self.user.id,
             'portfolio_id': self.portfolio.portfolio_id})
        expected_content.pop('date_created', None)
        self.assertEqual(expected_content, portfolio)

    def test_delete_portfolio_authorized_user(self):
        # delete the portfolio
        request = self.factory.get(
            reverse(
                'delete_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id}
            )
        )
        request.user = self.user
        response = api.delete_portfolio(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 200)

        # get the portfolio
        request = self.factory.get(
            reverse(
                'get_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id}
            )
        )
        request.user = self.user
        with self.assertRaises(Http404):
            api.get_portfolio(
                request, portfolio_id=self.portfolio.portfolio_id)

    def test_delete_portfolio_unauthorized_user(self):
        # delete the portfolio
        request = self.factory.get(
            reverse(
                'delete_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id}
            )
        )
        request.user = AnonymousUser()
        response = api.delete_portfolio(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 403)

        # get the portfolio
        request = self.factory.get(
            reverse(
                'get_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = AnonymousUser()
        response = api.get_portfolio(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 403)

    def test_get_portfolio_by_user_authorized_user(self):
        request = self.factory.get(
            reverse('get_portfolio_by_user', kwargs={'user_id': self.user.id})
        )
        request.user = self.user
        response = api.get_portfolio_by_user(request, self.user.id)
        self.assertEqual(response.status_code, 200)
        expected_content = json.loads(
            '{"risk_history": [], "portfolio_id": 1, "sector_allocations": {},'
            '"date_created": "2016-03-17 02:35:55.273000", "stocks": [], '
            '"portfolio_userid": 1, "name": null, "rank": null}')
        expected_content.update(
            {'portfolio_userid': self.user.id,
             'portfolio_id': self.portfolio.portfolio_id})
        expected_content.pop('date_created', None)
        received_content = json.loads(response.content)
        received_content.pop('date_created', None)
        self.assertEqual(expected_content, received_content)

    def test_get_portfolio_by_user_unauthorized_user(self):
        request = self.factory.get(
            reverse('get_portfolio_by_user', kwargs={'user_id': self.user.id})
        )
        request.user = AnonymousUser()
        response = api.get_portfolio_by_user(request, self.user.id)
        self.assertEqual(response.status_code, 403)

    def test_get_portfolio_by_user_non_existent_user(self):
        request = self.factory.get(
            reverse('get_portfolio_by_user', kwargs={'user_id': 100})
        )
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            api.get_portfolio_by_user(request, 100)

    def test_get_list_of_portfolios(self):
        request = self.factory.get(
            reverse('get_portfolio_list_by_user',
                    kwargs={'user_id': self.user.id})
        )
        request.user = self.user
        response = api.get_list_of_portfolios(request, self.user.id)
        self.assertEqual(response.status_code, 200)
        expected_content = {
            'portfolio_list': [{
                'id': self.portfolio.portfolio_id,
                'name': None}]}
        received_content = json.loads(response.content)
        self.assertEqual(expected_content, received_content)

    def test_get_list_of_portfolios_non_existent_user(self):
        request = self.factory.get(
            reverse('get_portfolio_list_by_user',
                    kwargs={'user_id': 100})
        )
        request.user = self.user
        with self.assertRaises(Http404):
            api.get_list_of_portfolios(request, 100)

    def test_get_portfolio_authorized_user(self):
        request = self.factory.get(
            reverse(
                'get_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = self.user
        request.portfolio = self.portfolio
        response = api.get_portfolio(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 200)
        expected_content = json.loads(
            '{"risk_history": [], "sector_allocations": {},'
            '"date_created": "2016-03-17 02:35:55.273000", "stocks": [], '
            '"name": null, "rank": null}')
        expected_content.update(
            {'portfolio_userid': self.user.id,
             'portfolio_id': self.portfolio.portfolio_id})
        expected_content.pop('date_created', None)
        received_content = json.loads(response.content)
        received_content.pop('date_created', None)
        self.assertEqual(expected_content, received_content)

    def test_get_portfolio_unauthorized_user(self):
        request = self.factory.get(
            reverse(
                'get_portfolio',
                kwargs={'portfolio_id': self.portfolio.portfolio_id})
        )
        request.user = AnonymousUser()
        request.portfolio = self.portfolio
        response = api.get_portfolio(
            request, portfolio_id=self.portfolio.portfolio_id)
        self.assertEqual(response.status_code, 403)

    def test_get_portfolio_non_existent_portfolio(self):
        request = self.factory.get(
            reverse('get_portfolio', kwargs={'portfolio_id': 100})
        )
        request.user = self.user
        with self.assertRaises(Http404):
            api.get_portfolio(request, portfolio_id=100)
