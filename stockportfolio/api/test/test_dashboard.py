import base64
import logging
import os
import time

import requests
from django.test import LiveServerTestCase
from registration.models import RegistrationProfile
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from stockportfolio.api.test.test_selenium import SeleniumTestCase
from stockportfolio.settings.base import BASE_DIR


class DashboardTest(SeleniumTestCase):
    """
    GUI testing for the dashboard
    """

    def setUp(self):
        """
        Setting up test fixture
        """

        self.cls = DashboardTest
        super(DashboardTest, self).setUp()

    def test_all(self):
        """
        Runs everything sequentially
        """

        self.cls.login()
        self.display_risk_rank()
        self.search_stock_no_stocks_exist()
        self.top_ten_loads()

    def display_risk_rank(self):
        """
        Tests if risk and rank exists
        """

        self.cls.driver.implicitly_wait(10)
        self.cls.driver.get(self.cls.live_server_url + '/dashboard/')
        WebDriverWait(
            self.cls.driver, 20).until(
                lambda driver: driver.find_element_by_tag_name('body'))
        self.assertEqual(
            self.cls.driver.title,
            'SPRA | {}\'s profile'.format(self.cls.user_info.get('user_name')))
        risk = self.cls.driver.find_element_by_id('portfolio_risk')
        self.assertEqual(risk.text, 'N/A')
        rank = self.cls.driver.find_element_by_id('risk_rank')
        self.assertEqual(rank.text, 'N/A')

    def search_stock_no_stocks_exist(self):
        """
        Tests if searching stock pops the suggestion
        and invokes stock interface also that correct
        warning is raised if stock does not exist
        """

        self.cls.driver.implicitly_wait(10)
        self.cls.driver.get(self.cls.live_server_url + '/dashboard/')
        WebDriverWait(
            self.cls.driver, 20).until(
                lambda driver: driver.find_element_by_id('search_entry'))
        self.assertEqual(
            self.cls.driver.title,
            'SPRA | {}\'s profile'.format(self.cls.user_info.get('user_name')))
        search_box = self.cls.driver.find_element_by_id('search_entry')
        search_box.send_keys('No')
        WebDriverWait(
            self.cls.driver, 60).until(
                lambda driver: driver.find_element_by_class_name('ac_results'))
        self.cls.driver.find_element_by_class_name('ac_results')

    def top_ten_loads(self):
        """
        Checks if top ten protfolio section is loaded
        """

        self.cls.driver.implicitly_wait(10)
        self.cls.driver.get(self.cls.live_server_url + '/dashboard/')
        WebDriverWait(
            self.cls.driver, 60).until(
                lambda driver: driver.find_element_by_id('top-portfolios'))
        self.cls.driver.find_element_by_id('top-portfolios').click()
        WebDriverWait(
            self.cls.driver, 60).until(
                lambda driver: driver.find_element_by_id('topPortfolios'))
        self.cls.driver.find_element_by_id('topPortfolios')
        self.cls.driver.find_element_by_class_name('top_portfolio_header')
        self.cls.driver.find_element_by_xpath(
            '//*[@id="topPortfolios"]/div[2]/div/div[1]/button').click()
        # self.cls.driver.execute_script('$("#topPortfolios").modal("hide")')
