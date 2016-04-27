#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
    
    def test_dashboard(self):
        SeleniumTestCase.driver.get(SeleniumTestCase.live_server_url + '/dashboard/')       
        self.wait(self.new_page, self.timeout)
        body = SeleniumTestCase.driver.find_element_by_tag_name('body')
        self.assertEqual(SeleniumTestCase.driver.title, 
            'SPRA | %s\'s profile' % (SeleniumTestCase.user_info['user_name']))
