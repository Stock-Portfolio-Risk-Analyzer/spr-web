from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import sys

class SeleniumTestCase(StaticLiveServerTestCase):
    
    def setUp(self):
        super(SeleniumTestCase, self).setUp()
        self.driver = webdriver.Firefox()       
        self.driver.maximize_window()
        self.timeout = 20
        self.un    = 'test_user'
        self.pw    = 'Passw0rd@1234'
        self.email = 'test@test.net'
        self.new_page = lambda driver: driver.find_element_by_tag_name('body')
        self.register_and_activate()
        self.login()
        self.create_portfolios()

    def tearDown(self):
        self.driver.quit()
        super(SeleniumTestCase, self).tearDown()
    
    def register_and_activate(self):
        self.driver.get(self.live_server_url+'/accounts/register/')
        username_box = self.driver.find_element_by_name('username')
        username_box.send_keys(self.un)
        email_box = self.driver.find_element_by_name('email')
        email_box.send_keys(self.email)
        password1_box = self.driver.find_element_by_name('password1')
        password1_box.send_keys(self.pw)
        password2_box = self.driver.find_element_by_name('password2')
        password2_box.send_keys(self.pw)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Submit')]").click() 
        test_profile = RegistrationProfile.objects.get(activated=False)
        test_user = test_profile.user
        test_user.is_active = True
        test_profile.activated = True
        test_user.save()
        test_profile.save()  
    
    def login(self):
        self.driver.get(self.live_server_url)
        WebDriverWait(self.driver, self.timeout).until(
                        EC.title_contains('Stock Portfolio Risk Analyzer')) 
        self.driver.find_element_by_partial_link_text('Login').click()
        # redirect to login
        self.wait(self.new_page)
        username_box = self.driver.find_element_by_id('id_username')
        username_box.send_keys(self.un)
        password_box = self.driver.find_element_by_id('id_password')
        password_box.send_keys(self.pw)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Sign in')]").click() 


    def create_portfolios(self):
        self.portfolios = []
        p1 = {'portfolio_name': 'test portfolio one',
              'stock_symbol'  : 'AAPL',
              'stock_amount'  : '10'}
        p2 = {'portfolio_name': 'test portfolio two',
              'stock_symbol'  : 'GOOG',
              'stock_amount'  : '3'}
        self.portfolios.append(p1)
        self.portfolios.append(p2)

    def wait(self, fn, time=20):
        WebDriverWait(self.driver, time).until(fn)

    def test_dashboard(self):
        self.driver.get(self.live_server_url + '/dashboard/')       
        self.wait(self.new_page, 60)
        body = self.driver.find_element_by_tag_name('body')
        self.assertEqual(self.driver.title, 'SPRA | %s\'s profile' % (self.un))
    
    def test_modify_account(self):
       ma = self.driver.find_elements_by_xpath("//*[@data-target='#userAccountModal']") 
       self.assertEqual(len(ma), 1)
       ma[0].click()
       username_box = self.driver.find_elements_by_xpath("//*[@value='%s']" % (self.un))[0]
       self.un = 'test_user_2'
       username_box.send_keys(self.un)
       self.driver.find_element_by_id('submit-id-submit').click() 

    def test_add_portfolios(self):
        self.assertEqual(self.driver.title, 'SPRA | %s\'s profile' % (self.un))
        for p in self.portfolios:
            add_btn  = self.driver.find_element_by_id('add-portfolio')
            add_btn.click()
            # fill out portfolio form
            portfolio_name = self.driver.find_element_by_id('pname')
            portfolio_name.send_keys(p['portfolio_name'])
            row_btn  = self.driver.find_element_by_id('add-row')
            save_btn = self.driver.find_element_by_id('save-button')
            row_btn.click()
            symbol = self.driver.find_element_by_id('symbol')
            symbol.send_keys(p['stock_symbol'])
            quantity = self.driver.find_element_by_id('quantity')
            quantity.send_keys(p['stock_amount'])
            save_btn.click()
    '''
    def test_persistent_portfolios(self):
        plist = self.driver.find_elements_by_class_name('portfolio-list')
        self.assertEqual(len(plist), 1) 
        portfolios = plist[0].find_elements_by_tag_name('li')
        self.assertEqual(plist[0], "")
        self.assertEqual(len(portfolios), 2)
        for p in portfolios:
            pname = p.find_elements_by_tag_name('a').text
            isName = self.portfolios[0]['portfolio_name'] == pname or self.portfolios[1]['portfolio_name'] == pname
            self.assertTrue(pname)
    '''

    def test_download_portfolio(self):
        dl_button = self.driver.find_element_by_id('download-portfolio')
        dl_button.click()

