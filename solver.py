from time import sleep, time
from urllib.parse import urlparse, parse_qs, unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Solver(object):
    def __init__(self, user_agent):
        options = webdriver.ChromeOptions()
        options.add_extension("Captcha-Solver-Auto-captcha-solving-service.crx")
        options.add_argument("--user-agent=" + user_agent)
        options.add_argument("--disable-cache")
        self.driver: WebDriver = webdriver.Remote(command_executor="http://192.168.54.4:4444/wd/hub", options=options)

    def prepare(self):
        print("Preparing captcha solver")
        self.driver.get('chrome-extension://pgojnojmmhpofjgdmaebadhbocahppod/www/index.html#/popup')

        wait = WebDriverWait(self.driver, 10)
        input_api_key = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'q-placeholder')))
        input_api_key.click()
        input_api_key.send_keys('CAP-38408BFA1C75A051232C8ADD0C969E0C')
        sleep(1)
        button_save = self.driver.find_element(By.CLASS_NAME, 'text-balance')
        button_save.click()
        sleep(1)
        print("Captcha solver ready")

    def intent_solve(self, url_captcha):
        print("Solving captcha")
        self.driver.get(url_captcha)

        start_solve = time()
        while True:
            url_now = self.driver.current_url
            if 'uniqueValidationId' in url_now:
                print("Captcha solved")
                return True

            if url_now != url_captcha:
                print("URL changed", url_captcha, url_now)

            if time() - start_solve > 60:
                print("Timeout reached while solving captcha")
                return False

            sleep(1)

    def clear_cache(self):
        self.driver.delete_all_cookies()
        print("Clearing cache")
        self.driver.get('chrome://settings/clearBrowserData')
        sleep(1)
        self.driver.find_element(By.XPATH, '//settings-ui').send_keys(Keys.ENTER)

    def solve(self, url_captcha):
        if self.intent_solve(url_captcha):
            parsed_url = urlparse(self.driver.current_url)
            query_params = parse_qs(parsed_url.query)
            session_token = query_params['sessionToken'][0]
            return unquote(session_token)
