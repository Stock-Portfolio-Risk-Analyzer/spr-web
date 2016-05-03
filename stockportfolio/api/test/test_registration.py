from registration.models import RegistrationProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from stockportfolio.api.test.test_selenium import SeleniumTestCase


class RegistrationTestCase(SeleniumTestCase):
    """
    GUI testing for user registration
    """

    def setUp(self):
        """
        Test fixture 
        """
        self.cls = RegistrationTestCase
        super(RegistrationTestCase, self).setUp()
        self.cls.user_info['user_name'] = 'register_user'

    def tearDown(self):
        """
        Test fixture 
        """
        super(RegistrationTestCase, self).tearDown()

    @classmethod
    def setUpClass(cls):
        """
        Creates the Selenium driver and activates a user account
        This is a class method, so it runs before any tests.
        """
        super(RegistrationTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Runs at the end of all the tests. Stops the web driver
        """
        super(RegistrationTestCase, cls).tearDownClass()
    
    def test_runner(self):
        """
        Runs everything sequentially
        """
        self.landing()
        self.register()
        self.register_complete()
        self.activation()

    def landing(self):
        """
        Checks if landing page is rendered
        """

        self.cls.driver.get(self.cls.live_server_url)
        WebDriverWait(self.cls.driver, self.timeout).until(
            EC.title_contains('Stock Portfolio Risk Analyzer'))
        headings = self.cls.driver.find_elements_by_class_name('headings')
        self.assertEqual(len(headings), 2)
        inners = self.cls.driver.find_elements_by_class_name(
            'header-content-inner')
        self.assertEqual(len(inners), 1)
        inner_header = inners[0]
        h1s = inner_header.find_elements_by_tag_name('h1')
        self.assertEqual(len(h1s), 1)
        self.assertEqual(h1s[0].text.lower(),
                         'get deeper insights into your portfolio')
        # redirect to registration page
        button = self.cls.driver.find_element_by_xpath(
            '//*[@id="page-top"]/header/div/div/a[1]')
        #self.wait(self.new_page)
        self.cls.driver.implicitly_wait(10)
        button.click()

    def register(self):
        """
        Checks if register functionality works
        """
        #self.cls.driver.get(self.cls.live_server_url)
        #self.assertEqual(self.cls.driver.title, 'User test')
        username_box = self.cls.driver.find_element_by_name('username')
        username_box.send_keys(self.cls.user_info['user_name'])
        email_box = self.driver.find_element_by_name('email')
        email_box.send_keys(self.cls.user_info['email'])
        password1_box = self.driver.find_element_by_name('password1')
        password1_box.send_keys(self.cls.user_info['password'])
        password2_box = self.driver.find_element_by_name('password2')
        password2_box.send_keys(self.cls.user_info['password'])
        self.driver.find_element_by_xpath(
            "//*[contains(text(), 'Submit')]").click()
        self.cls.driver.implicitly_wait(100)

    def register_complete(self):
        """
        Checks if register was succesfully completed
        """

        self.assertEqual(self.cls.driver.title, 'User test')
        content = self.cls.driver.find_element_by_id('content')
        message = content.find_elements_by_tag_name('p')
        self.assertEqual(message[0].text,
                         'You are now registered. Activation email sent.')

    def activation(self):
        """
        Checks if activation worked
        """

        test_profile = RegistrationProfile.objects.get(activated=False)
        test_user = test_profile.user
        self.assertFalse(test_profile.activated)
        self.assertFalse(test_user.is_active)
        test_user.is_active = True
        test_profile.activated = True
        test_user.save()
        test_profile.save()
