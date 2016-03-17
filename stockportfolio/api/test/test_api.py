import unittest
import stockportfolio.api.api as api
from django.conf.urls import url
from django.core.urlresolvers import reverse

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = 'thibaut.xiong@gmail.com'

    def test_get_portfolio(self):
        # url(r'^portfolio/(?P<portfolio_id>\d+)$', api.get_portfolio, name="get_portfolio"),
        return True