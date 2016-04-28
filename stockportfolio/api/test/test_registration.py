from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from registration.models import RegistrationProfile

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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

    def tearDown(self):
        self.driver.quit()
        super(SeleniumTestCase, self).tearDown()
    
    def test_runner(self):
        self.landing()
        self.register()
        self.register_complete()
        self.activation()
        self.confirm_activation()
        self.login()
        self.dashboard()

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
        self.wait(self.new_page, 20)
        self.driver.get(self.live_server_url + '/dashboard/')       
        self.wait(self.new_page, 60)
        body = self.driver.find_element_by_tag_name('body')
        self.assertEqual(self.driver.title, 'SPRA | %s\'s profile' % (self.un))
