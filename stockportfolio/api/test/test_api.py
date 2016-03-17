import unittest
import stockportfolio.api.api as api
from django.conf.urls import url

class TestAPI(unittest.TestCase):

    @classmethod
    def setUp(self):
        cls.user = 'thibaut.xiong@gmail.com'

    # def test_add_stock(self):
        url(r'^portfolio/(?P<portfolio_id>\d+)/addstock$', api.add_stock, name="add_stock"),
