import base64
import os
import time

import requests
from django.test import LiveServerTestCase
from registration.models import RegistrationProfile
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from stockportfolio.settings.base import BASE_DIR


class SeleniumTestCase(LiveServerTestCase):

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
        super(SeleniumTestCase, cls).setUpClass()
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
        WebDriverWait(SeleniumTestCase.driver, time).until(fn)

    def test_dashboard(self):
        SeleniumTestCase.driver.get(
            SeleniumTestCase.live_server_url + '/dashboard/')
        self.wait(self.new_page, self.timeout)
        SeleniumTestCase.driver.find_element_by_tag_name('body')
        self.assertEqual(
            SeleniumTestCase.driver.title,
            'SPRA | %s\'s profile' % (SeleniumTestCase.user_info['user_name']))
 
    def test_modify_account(self):
       cls = SeleniumTestCase
       cls.driver.implicitly_wait(10)
       dropdown = cls.driver.find_elements_by_class_name('user-profile')[0]
       dropdown.click()
       ma = cls.driver.find_elements_by_xpath("//*[@data-target='#userAccountModal']") 
       self.assertEqual(len(ma), 1)
       ma[0].click()
       username_box = cls.driver.find_elements_by_xpath("//*[@value='%s']" % (cls.user_info['user_name']))[0]
       cls.user_info['user_name'] = 'test_user_2'
       wait = WebDriverWait(cls.driver, 60)
       wait.until(EC.visibility_of_element_located((By.ID, 'id_username')))
       username_box.send_keys(SeleniumTestCase.user_info['user_name'])
       SeleniumTestCase.driver.find_element_by_id('submit-id-submit').click() 

    '''
    def test_add_portfolios(self):
        cls = SeleniumTestCase
        SeleniumTestCase.driver.get(SeleniumTestCase.live_server_url + '/dashboard/')       
        self.wait(self.new_page, self.timeout)
        self.assertEqual(cls.driver.title, 'SPRA | %s\'s profile' % (cls.user_info['user_name']))
        for p in cls.portfolios:
            add_btn  = cls.driver.find_element_by_id('add-portfolio')
            WebDriverWait(cls.driver, 60)
            add_btn.click()
            wait = WebDriverWait(cls.driver, 60)
            wait.until(EC.visibility_of_element_located((By.ID, 'pname')))
            # fill out portfolio form
            portfolio_name = cls.driver.find_element_by_id('pname')
            portfolio_name.send_keys(p['portfolio_name'])
            row_btn  = cls.driver.find_element_by_id('add-row')
            save_btn = cls.driver.find_element_by_id('save-button')
            row_btn.click()
            ac = ActionChains(cls.driver)
            t = cls.driver.find_elements_by_class_name('modal-title')
            ac.move_to_element(t[0]).move_by_offset(0,0).click().perform()
            wait = WebDriverWait(cls.driver, 60)
            wait.until(EC.visibility_of_element_located((By.ID, 'quantity')))
            symbol = cls.driver.find_element_by_id('symbol')
            symbol.send_keys(p['stock_symbol'])
            quantity = cls.driver.find_element_by_id('quantity')
            quantity.send_keys(p['stock_amount'])
            save_btn.click()
    '''
    def test_import_export_portfolio(self):
        cls = SeleniumTestCase
        dl_button = cls.driver.find_element_by_id('download-portfolio')
        self.assertEqual(dl_button.text, 'Export Portfolio (csv)')
        ul_button = cls.driver.find_element_by_id('upload-portfolio')
        #self.assertEqual(ul_button.text, 'Import Portfolio (csv)')



    def test_generated_portfolio(self):
        cls = SeleniumTestCase
        gen_button = cls.driver.find_element_by_id('generate-portfolio')
        self.assertEqual(gen_button.text, 'Generate Portfolio')
        #gen_button.click()
        #x = cls.driver.find_elements_by_xpath("//*[@data-dismiss='modal']") 
        #x.click()
    