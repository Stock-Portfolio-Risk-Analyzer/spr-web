import base64
import logging
import os
import time

import requests
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from registration.models import RegistrationProfile
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from stockportfolio.settings.base import BASE_DIR


class SeleniumTestCase(LiveServerTestCase):
    driver = None
    user_info = {
        'user_name': 'test_user',
        'password': 'Passw0rd@1234',
        'email': 'test@test.net',
    }

    portfolios = [ {'portfolio_name': 'test portfolio one',
                    'stock_symbol'  : 'AAPL',
                     'stock_amount'  : '10'},
                   {'portfolio_name': 'test portfolio two',
                    'stock_symbol'  : 'GOOG',
                    'stock_amount'  : '3'}]

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestCase, cls).setUpClass()
        LOGGER.setLevel(logging.WARNING)
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.register_and_activate()
        cls.login()

    def setUp(self):
        self.new_page = lambda driver: driver.find_element_by_tag_name('body')
        self.timeout = 20

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    @classmethod
    def register_and_activate(cls):
        cls.driver.get(cls.live_server_url+'/accounts/register/')
        username_box = cls.driver.find_element_by_name('username')
        username_box.send_keys(cls.user_info['user_name'])
        email_box = cls.driver.find_element_by_name('email')
        email_box.send_keys(cls.user_info['email'])
        password1_box = cls.driver.find_element_by_name('password1')
        password1_box.send_keys(cls.user_info['password'])
        password2_box = cls.driver.find_element_by_name('password2')
        password2_box.send_keys(cls.user_info['password'])
        cls.driver.find_element_by_xpath("//*[contains(text(), 'Submit')]").click()
        test_profile = RegistrationProfile.objects.get(activated=False)
        test_user = test_profile.user
        test_user.is_active = True
        test_profile.activated = True
        test_user.save()
        test_profile.save()

    @classmethod
    def login(cls):
        cls.driver.get(cls.live_server_url)
        WebDriverWait(cls.driver, 20).until(
                        EC.title_contains('Stock Portfolio Risk Analyzer'))
        cls.driver.find_element_by_xpath("//*[contains(text(), 'Login')]").click()
        WebDriverWait(cls.driver, 20).until(lambda driver: driver.find_element_by_tag_name('body'))
        username_box = cls.driver.find_element_by_id('id_username')
        username_box.send_keys(cls.user_info['user_name'])
        password_box = cls.driver.find_element_by_id('id_password')
        password_box.send_keys(cls.user_info['password'])
        cls.driver.find_element_by_xpath("//*[contains(text(), 'Sign in')]").click()

    def wait(self, fn, time=20):
        WebDriverWait(SeleniumTestCase.driver, time).until(fn)

    def screenshot(self, prefix="", upload=True):
        """
        :param prefix: optional prefix for the resulting file
        :param upload: upload the image to Imgur (default)
        """
        fname = os.path.join(
                            BASE_DIR, 'api', 'test', 
                            prefix + '_' + str(time.time()) + '.png')
        self.cls.driver.save_screenshot(fname)
        with open(fname, "rb") as img:
            b64 = base64.b64encode(img.read())
            if upload:
                r = requests.post('https://api.imgur.com/3/image',
                                  data={'image':b64},
                                  headers={'Authorization':'Client-ID 5adddc48c3f790d'})
                print 'image link ' + r.content

class DashboardTest(SeleniumTestCase):

    def setUp(self):
        self.cls = DashboardTest
        super(DashboardTest, self).setUp()

    def test_all(self):
        self.display_risk_rank()
        self.search_stock_no_stocks_exist()
        self.top_ten_loads()

    def display_risk_rank(self):
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
        self.cls.driver.implicitly_wait(10)
        self.cls.driver.get(self.cls.live_server_url + '/dashboard/')
        WebDriverWait(
            self.cls.driver, 60).until(
                lambda driver: driver.find_element_by_id('top-portfolios'))
        self.screenshot(prefix='top_ten_loads')
        self.cls.driver.find_element_by_id('top-portfolios').click()
        WebDriverWait(
            self.cls.driver, 60).until(
                lambda driver: driver.find_element_by_id('topPortfolios'))
        modal = self.cls.driver.find_element_by_id('topPortfolios')
        self.cls.driver.find_element_by_class_name('top_portfolio_header')
        self.cls.driver.find_element_by_xpath('//*[@id="topPortfolios"]/div[2]/div/div[1]/button')
        self.cls.driver.execute_script('$("#topPortfolios").modal("hide")')
