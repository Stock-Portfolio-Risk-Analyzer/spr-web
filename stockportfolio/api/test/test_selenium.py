from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from registration.models import RegistrationProfile

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumTestCase(StaticLiveServerTestCase):
    
    def setUp(self):
        super(SeleniumTestCase, self).setUp()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.timeout = 20
        self.new_page = lambda driver: driver.find_element_by_tag_name('body')
        self.un    = 'test_user'
        self.pw    = 'Passw0rd@1234'
        self.email = 'test@test.net'
        self.create_portfolios()
    
    def tearDown(self):
        self.driver.quit()
        super(SeleniumTestCase, self).tearDown()
    
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

    def test_runner(self):
        self.landing()
        self.register()
        self.register_complete()
        self.activation()
        self.confirm_activation()
        self.login()
        self.dashboard()
        #self.modify_account()
        self.add_portfolios()
        #self.persistent_portfolios()

    def wait(self, fn, time=20):
        WebDriverWait(self.driver, time).until(fn)

    def landing(self):
        self.driver.get(self.live_server_url)
        WebDriverWait(self.driver, self.timeout).until(
                        EC.title_contains('Stock Portfolio Risk Analyzer'))
        headings = self.driver.find_elements_by_class_name('headings')
        self.assertEqual(len(headings), 2)
        inners = self.driver.find_elements_by_class_name('header-content-inner')
        self.assertEqual(len(inners), 1)
        inner_header = inners[0]
        h1s = inner_header.find_elements_by_tag_name('h1')
        self.assertEqual(len(h1s), 1)
        self.assertEqual(h1s[0].text,
                    'Get Deeper Insights Into Your Portfolio')
        # redirect to registration page
        self.driver.find_element_by_partial_link_text('Sign Up').click()
        self.wait(self.new_page) 

    def register(self):
        self.assertEqual(self.driver.title, 'User test')
        username_box = self.driver.find_element_by_name('username')
        username_box.send_keys(self.un)
        email_box = self.driver.find_element_by_name('email')
        email_box.send_keys(self.email)
        password1_box = self.driver.find_element_by_name('password1')
        password1_box.send_keys(self.pw)
        password2_box = self.driver.find_element_by_name('password2')
        password2_box.send_keys(self.pw)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Submit')]").click() 
        # redirect to registration completion page
        self.wait(self.new_page)        

    def register_complete(self):
         self.assertEqual(self.driver.title, 'User test')
         content = self.driver.find_element_by_id('content')
         message = content.find_elements_by_tag_name('p')
         self.assertEqual(len(message), 1)
         self.assertEqual(message[0].text, 
                          'You are now registered. Activation email sent.')

    def activation(self):
        test_profile = RegistrationProfile.objects.get(activated=False)
        test_user = test_profile.user
        self.assertFalse(test_profile.activated)
        self.assertFalse(test_user.is_active)
        test_user.is_active = True
        test_profile.activated = True
        test_user.save()
        test_profile.save()         
    
    def confirm_activation(self):
        profile = RegistrationProfile.objects.get(activated=True)
        self.assertTrue(profile.activated)
        self.assertTrue(profile.user.is_active)

    def login(self):
        self.driver.get(self.live_server_url)
        WebDriverWait(self.driver, self.timeout).until(
                        EC.title_contains('Stock Portfolio Risk Analyzer')) 
        self.driver.find_element_by_partial_link_text('Login').click()
        # redirect to login
        self.wait(self.new_page)
        self.assertEqual(self.driver.title, 'User test')
        username_box = self.driver.find_element_by_id('id_username')
        username_box.send_keys(self.un)
        password_box = self.driver.find_element_by_id('id_password')
        password_box.send_keys(self.pw)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Sign in')]").click() 
            
    def dashboard(self):
        self.driver.get(self.live_server_url + '/dashboard/')       
        self.wait(self.new_page, 60)
        body = self.driver.find_element_by_tag_name('body')
        self.assertEqual(self.driver.title, 'SPRA | %s\'s profile' % (self.un))
    
    def modify_account(self):
       ma = self.driver.find_elements_by_xpath("//*[@data-target='#userAccountModal']") 
       self.assertEqual(len(ma), 1)
       ma[0].click()
       username_box = self.driver.find_elements_by_xpath("//*[@value='%s']" % (self.un))[0]
       self.un = 'test_user_2'
       username_box.send_keys(self.un)
       self.driver.find_element_by_id('submit-id-submit').click() 

    def add_portfolios(self):
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
    
    def persistent_portfolios(self):
        plist = self.driver.find_elements_by_class_name('portfolio-list')
        self.assertEqual(len(plist), 1) 
        portfolios = plist[0].find_elements_by_tag_name('li')
        self.assertEqual(plist[0], "")
        self.assertEqual(len(portfolios), 2)
        for p in portfolios:
            pname = p.find_elements_by_tag_name('a').text
            isName = self.portfolios[0]['portfolio_name'] == pname or self.portfolios[1]['portfolio_name'] == pname
            self.assertTrue(pname)

    def download_portfolio(self):
        dl_button = self.driver.find_element_by_id('download-portfolio')
        dl_button.click()

