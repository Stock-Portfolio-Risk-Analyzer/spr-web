from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from stockportfolio.api.models import Portfolio
from stockportfolio.api import api
import json


class ApiTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='testing123')
        self.portfolio = Portfolio.objects.create(portfolio_user=self.user)
        self.portfolio.save()

    def test_add_stock(self):
        raise NotImplementedError()

    def test_get_portfolio_by_user(self):
        # url(r'^user/(?P<user_id>\d+)/getportfolio', api.get_portfolio_by_user, name="get_portfolio_by_user"),

        request = self.factory.get(
            reverse('get_portfolio_by_user', kwargs={'user_id': self.user.id}))
        request.user = self.user
        response = api.get_portfolio_by_user(request, self.user.id)
        self.assertEqual(response.status_code, 200)
        expected_content = json.loads('{"risk_history": [], "portfolio_id": 1, "sector_allocations": {}, "date_created": "2016-03-17 02:35:55.273000", "stocks": [], "portfolio_userid": 1}')
        expected_content.pop('date_created', None)
        received_content = json.loads(response.content)
        received_content.pop('date_created', None)
        self.assertEqual(expected_content, received_content)

    def test_get_portfolio(self):
        # url(r'^portfolio/(?P<portfolio_id>\d+)$', api.get_portfolio, name="get_portfolio"),
        request = self.factory.get(
            reverse('get_portfolio', kwargs={'portfolio_id': 1})
        )
        request.portfolio = self.portfolio
        response = api.get_portfolio(request, portfolio_id=1)
        self.assertEqual(response.status_code, 200)
        expected_content = json.loads('{"risk_history": [], "portfolio_id": 1, "sector_allocations": {}, "date_created": "2016-03-17 02:35:55.273000", "stocks": [], "portfolio_userid": 1}')
        expected_content.pop('date_created', None)
        received_content = json.loads(response.content)
        received_content.pop('date_created', None)
        self.assertEqual(expected_content, received_content)