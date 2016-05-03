from registration.models import RegistrationProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from stockportfolio.api.test.test_selenium import SeleniumTestCase


class ModifyAccountTestCase(SeleniumTestCase):
    """
    GUI testing for account modification
    """

    def setUp(self):
        """
        Test fixture 
        """
        self.cls = ModifyAccountTestCase
        super(ModifyAccountTestCase, self).setUp()

    def tearDown(self):
        """
        Test fixture 
        """
        super(ModifyAccountTestCase, self).tearDown()

    @classmethod
    def setUpClass(cls):
        """
        Creates the Selenium driver and activates a user account
        This is a class method, so it runs before any tests.
        """
        super(ModifyAccountTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Runs at the end of all the tests. Stops the web driver
        """
        super(ModifyAccountTestCase, cls).tearDownClass()

    def test_dashboard(self):
        """
        Test that we can load the dashboard completely
        """
        self.cls.login()
        self.cls.driver.get(
            self.cls.live_server_url + '/dashboard/')
        #self.wait(self.new_page, self.timeout)
        self.cls.driver.find_element_by_tag_name('body')
        self.assertEqual(
            self.cls.driver.title,
            'SPRA | %s\'s profile' % (self.cls.user_info['user_name']))
 
    def test_modify_account(self):
        """
        Test that we can load the modify account modal and change account
        details
        """
        
        self.cls.driver.implicitly_wait(10)
        dropdown = self.cls.driver.find_elements_by_class_name('user-profile')[0]
        dropdown.click()
        ma = self.cls.driver.find_elements_by_xpath("//*[@data-target='#userAccountModal']") 
        self.assertEqual(len(ma), 1)
        ma[0].click()
        username_box = self.cls.driver.find_elements_by_xpath(
        "//*[@value='%s']" % (self.cls.user_info['user_name']))[0]
        self.cls.user_info['user_name'] = 'test_user_2'
        wait = WebDriverWait(self.cls.driver, 60)
        wait.until(EC.visibility_of_element_located((By.ID, 'id_username')))
        username_box.send_keys(self.cls.user_info['user_name'])
        self.cls.driver.find_element_by_id('submit-id-submit').click() 
