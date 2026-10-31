from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class QueuePage:
    IDENTITY = (By.CSS_SELECTOR, '[data-test="staff-identity"]')
    CUSTOMER = (By.CSS_SELECTOR, '[data-test="customer-id"]')
    SERVICE = (By.CSS_SELECTOR, '[data-test="service"]')
    ISSUE = (By.CSS_SELECTOR, '[data-test="issue-ticket"]')
    MESSAGE = (By.CSS_SELECTOR, '[data-test="ticket-message"]')
    ROWS = (By.CSS_SELECTOR, '[data-test="ticket-row"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def identity(self):
        return self.wait.until(EC.visibility_of_element_located(self.IDENTITY)).text

    def issue(self, customer, service):
        field = self.wait.until(EC.visibility_of_element_located(self.CUSTOMER))
        field.clear()
        field.send_keys(customer)
        Select(self.driver.find_element(*self.SERVICE)).select_by_visible_text(service)
        self.wait.until(EC.element_to_be_clickable(self.ISSUE)).click()
        # The app publishes the final message only after refreshing the ticket table.
        self.wait.until(lambda d: d.find_element(*self.MESSAGE).text not in ('',))
        self.wait.until(EC.element_to_be_clickable(self.ISSUE))
        return self.driver.find_element(*self.MESSAGE).text

    def rows(self):
        return [[cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
                for row in self.driver.find_elements(*self.ROWS)]
