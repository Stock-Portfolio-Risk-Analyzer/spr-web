import base64
import os
import time

import requests
from django.test import LiveServerTestCase
from registration.models import RegistrationProfile

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from stockportfolio.settings.base import BASE_DIR


class SeleniumTestCase(LiveServerTestCase):
    """
    Base test case for Selenium tests.
    """

    driver = None
    user_info = {
        'user_name': 'test_user',
        'password': 'Passw0rd@1234',
        'email': 'test@test.net',
    }

    portfolios = [{'portfolio_name': 'test portfolio one',
                   'stock_symbol': 'AAPL',
                   'stock_amount': '10'},
                  {'portfolio_name': 'test portfolio two',
                   'stock_symbol': 'GOOG',
                   'stock_amount': '3'}]

    @classmethod
    def setUpClass(cls):
        """
        Creates the Selenium driver and activates a user account
        This is a class method, so it runs before any tests.
        """
        super(SeleniumTestCase, cls).setUpClass()
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.register_and_activate()

    def setUp(self):
        """
        Runs before each test and adds some helper methods/members
        """
        self.new_page = lambda driver: driver.find_element_by_tag_name('body')
        self.timeout = 20

    @classmethod
    def tearDownClass(cls):
        """
        Runs at the end of all the tests. Stops the web driver
        """
        cls.driver.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    @classmethod
    def register_and_activate(cls):
        """
        Class helper method that register and activates an account
        through Selenium
        """
        cls.driver.get(cls.live_server_url + '/accounts/register/')
        username_box = cls.driver.find_element_by_name('username')
        username_box.send_keys(cls.user_info['user_name'])
        email_box = cls.driver.find_element_by_name('email')
        email_box.send_keys(cls.user_info['email'])
        password1_box = cls.driver.find_element_by_name('password1')
        password1_box.send_keys(cls.user_info['password'])
        password2_box = cls.driver.find_element_by_name('password2')
        password2_box.send_keys(cls.user_info['password'])
        cls.driver.find_element_by_xpath(
            "//*[contains(text(), 'Submit')]").click()
        test_profile = RegistrationProfile.objects.get(activated=False)
        test_user = test_profile.user
        test_user.is_active = True
        test_profile.activated = True
        test_user.save()
        test_profile.save()

    @classmethod
    def login(cls):
        """
        Class helper method that logins the user before tests start running
        """
        cls.driver.get(cls.live_server_url)
        WebDriverWait(cls.driver, 20).until(
            EC.title_contains('Stock Portfolio Risk Analyzer'))
        cls.driver.find_element_by_xpath(
            "//*[contains(text(), 'Login')]").click()
        WebDriverWait(cls.driver, 20).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        username_box = cls.driver.find_element_by_id('id_username')
        username_box.send_keys(cls.user_info['user_name'])
        password_box = cls.driver.find_element_by_id('id_password')
        password_box.send_keys(cls.user_info['password'])
        cls.driver.find_element_by_xpath(
            "//*[contains(text(), 'Sign in')]").click()

    def screenshot(self, prefix="", upload=True):
        """
        Takes a screenshot of the page and optionally uploads it to Imgur
        Useful for getting screenshots out of Travis CI

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
                r = requests.post(
                    'https://api.imgur.com/3/image',
                    data={'image': b64},
                    headers={'Authorization': 'Client-ID 5adddc48c3f790d'})
                print 'image link ' + r.content

    def wait(self, fn, time=20):
        """
        Helper function to force Selenium to wait for a certain condition

        :param fn : (int) function that determines if we're done waiting
        :param time: time in seconds to wait before throwing TimeoutException
        """
        WebDriverWait(SeleniumTestCase.driver, time).until(fn)
