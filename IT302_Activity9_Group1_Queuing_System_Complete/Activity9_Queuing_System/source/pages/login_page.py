from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    USERNAME = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    SUBMIT = (By.CSS_SELECTOR, '[data-test="login-submit"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="login-error"]')

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.base_url + '/login')
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        return self

    def submit(self, username, password):
        for locator, value in [(self.USERNAME, username), (self.PASSWORD, password)]:
            field = self.wait.until(EC.visibility_of_element_located(locator))
            field.clear()
            field.send_keys(value)
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT)).click()

    def error_containing(self, text):
        self.wait.until(EC.text_to_be_present_in_element(self.ERROR, text))
        return self.driver.find_element(*self.ERROR).text
