""" Modules import """
from time import sleep

from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class Linkedin():
    """
    Use LinkedIn social media.

    Variables:
        linkedin {str} -- url web page

    """

    linkedin = 'https://www.linkedin.com/login/'

    def __init__(self, driver, email, password):
        """
        Initialize webdriver.
        """

        self.driver = driver
        self.email = email
        self.password = password
        self.website = Linkedin.linkedin

        self.chrome = webdriver.Chrome(self.driver)
        self.chrome.wait = WebDriverWait(self.chrome, 5)
        self.chrome.maximize_window()


    def login(self):
        """
        Login on LinkedIn.
        """

        self.chrome.get(self.website)

        try:
            user_field = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'username')))

            user_field.send_keys(self.email)
            user_field.send_keys(Keys.TAB)
        except TimeoutException as error:
            print('Username field not found.', str(error))

        try:
            pw_field = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'password')))

            pw_field.send_keys(self.password)
        except TimeoutException as error:
            print('Password field not found.', str(error))

        try:
            login_button = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.CLASS_NAME, 'login__form_action_container')))
            login_button.click()
        except TimeoutException as error:
            print('Login button not found.', str(error))

        self.minimize_window_msg()


    def minimize_window_msg(self):
        """
        Minimize chat bubble.
        """

        try:
            msg = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.CLASS_NAME, 'msg-overlay-bubble-header')))
            msg.click()
        except TimeoutException as error:
            print('Chat window element not found.', str(error))


    def logout(self):
        """
        Logout from LinkedIn.
        """

        try:
            me_button = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'ember22')))
            me_button.click()
        except TimeoutException as error:
            print('User button not found.', str(error))

        try:
            out_button = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'ember40')))
            out_button.click()
        except TimeoutException as error:
            print('Logout button not found.', str(error))

        self.chrome.quit()


class Vagas():
    """
    Use Vagas web job plataform.

    Variables:
        vagas {str} -- url web page

    """

    vagas = 'https://www.vagas.com.br/login-candidatos'

    def __init__(self, driver, email, password):
        """
        Initialize webdriver.
        """

        self.driver = driver
        self.email = email
        self.password = password
        self.website = Vagas.vagas

        self.chrome = webdriver.Chrome(self.driver)
        self.chrome.wait = WebDriverWait(self.chrome, 5)
        self.chrome.maximize_window()


    def login(self):
        """
        Login on Vagas.
        """

        self.chrome.get(self.website)

        try:
            user_field = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'login_candidatos_form_usuario')))

            user_field.send_keys(self.email)
            user_field.send_keys(Keys.TAB)
            sleep(0.5)
        except TimeoutException as error:
            print('Username field not found.', str(error))

        try:
            pw_field = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'login_candidatos_form_senha')))

            pw_field.send_keys(self.password)
        except TimeoutException as error:
            print('Password field not found.', str(error))

        try:
            login_button = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'submitLogin')))

            sleep(0.5)
            login_button.submit()
        except TimeoutException as error:
            print('Login button not found.', str(error))


    def logout(self):
        """
        Logout from Vagas.
        """

        try:
            candidate_button_menu = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'menu-candidatos-holder')))
            candidate_button_menu.click()
        except TimeoutException as error:
            print('Menu button not found.', str(error))

        try:
            out_button = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.LINK_TEXT, 'Sair')))
            out_button.click()
        except TimeoutException as error:
            print('Logout button not found.', str(error))

        self.chrome.quit()
