from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class SeleniumTest(StaticLiveServerTestCase):
    
    def setUp(self):
        super(SeleniumTest, self).setUpClass()
        self.selenium = webdriver.Chrome()
        #self.factory = RequestFactory()
        #self.user = User.objects.create_user(
        #                username='bane', email='test@example.com', 
        #                password='4uuuu@CIA')

    def tearDown(self):
        self.selenium.quit()
        super(SeleniumTest, self).tearDownClass()

    def test_dispatch(self):
        #self._registration()
        #self._dashboard()
        self.selenium.get(self.live_server_url)
        self.assertEqual(self.live_server_url, '')

    def _registration(self):
        """
        Test account creation from landing page
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_partial_link_text("Sign Up")
        # wait for response
        WebDriverWait(self.selenium, timeout).until(
                lambda driver: driver.find_element_by_tag_name('body'))
        # should be redirected to registration page
        username_box = self.selenium.find_element_by_name("username")
        username_box.send_keys('test_user')
        email_box = self.selenium.find_element_by_name("email")
        email_box.send_keys('test@email.test')
        password1_box = self.selenium.find_element_by_name("password1")
        password1_box.send_keys('password')
        password2_box = self.selenium.find_element_by_name("password2")
        password2_box.send_keys('password')
        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click() 
        WebDriverWait(self.selenium, timeout).until(
                lambda driver: driver.find_element_by_tag_name('body'))


    def _dashboard(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/logout'))


