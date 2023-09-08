import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webdriver_manager.firefox import GeckoDriverManager
import webdriver_manager.chrome import ChromeDriverManager

with open('./testdata.yaml') as f:
    testdata = yaml.safe_load(f)
    browser = testdata['browser']


class Site:
    def __init__(self,address):
        if browser == 'firefox':
            service = Service(executable_path=GeckoDriverManager().install())
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(service=service, options=options)
        elif browser == 'chrome':
            service = Service(executable_path=ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(testdata['implicitly_wait'])
        self.driver.maximize_window()
        self.driver.get(address)
        time.sleep(testdata['sleep_time'])

    def find_element(self, mode, path):
        if mode == 'css':
            element = self.driver.find_element(By.CSS_SELECTOR, path)
        elif mode == 'path':
            element = self.driver.find_element(By.XPATH, path)
        else:
            element = None
        return element

    def get_element_property(self, mode, path, property):
        element = self.find_element(mode, path)
        return element.value_of_css_property(property)

    def close(self):
        self.driver.close()

    def create_post(self, post_title, post_description, post_content):
        title_locator = '//*[@id="app"]/main/div/div[3]/div[1]/a[3]/h2'
        description_locator = '//*[@id="app"]/main/div/div[3]/div[1]/a[3]/div'
        content_locator = '//*[@id="app"]/main/div/div[3]/div[1]/a[3]/img'
        create_button_locator = '//*[@id="create-btn"]'

        title_input = self.find_element('xpath', title_locator)
        title_input.send_keys(post_title)

        description_input = self.find_element('xpath', description_locator)
        description_input.send_keys(post_description)

        content_input = self.find_element('xpath', content_locator)
        content_input.send_keys(post_content)

        create_button = self.find_element('xpath', create_button_locator)
        create_button.click()

    def check_post_existence(self, post_title):
        posts_locator = '//*[@id="app"]/main/div'

        self.driver.get("https://test-stand.gb.ru/")

        wait = WebDriverWait(self.driver, 10)
        posts_element = wait.until(EC.visibility_of_element_located((By.XPATH, posts_locator)))

        if post_title in posts_element.text:
            return True
        else:
            return False

    def wait_for_element_to_be_visible(self, mode, path):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, path))
            )
            return element
        except Exception as e:
            # Обработка исключения или вывод сообщения о том, что элемент не стал видимым
            pass
    def open_contact_us_form(self):
        open_form_button_locator = '//*[@id="app"]/main/nav/ul/li[2]/a'
        open_form_button = self.find_element('xpath', open_form_button_locator)

        open_form_button.click()

        contact_us_form_locator = '//*[@id="app"]/main/div'
        self.wait_for_element_to_be_visible('xpath', contact_us_form_locator)

    def enter_contact_us_details(self, name, email, message):
        name_input_locator = '//*[@id="contact"]/div[1]/label/input'
        name_input = self.find_element('xpath', name_input_locator)
        name_input.send_keys(name)

        email_input_locator = '//*[@id="contact"]/div[2]/label/input'
        email_input = self.find_element('xpath', email_input_locator)
        email_input.send_keys(email)

        message_input_locator = '//*[@id="contact"]/div[3]/label/span/textarea'
        message_input = self.find_element('xpath', message_input_locator)
        message_input.send_keys(message)

    def submit_contact_us_form(self):
        send_button_locator = '//*[@id="contact"]/div[4]/button/div'
        send_button = self.find_element('xpath', send_button_locator)
        send_button.click()

        alert = self.driver.switch_to.alert

        # Получаем текст из alert
        alert_text = alert.text

        # Закрываем alert
        alert.accept()

        return alert_text
