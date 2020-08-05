""" Modules import """
import re
from time import sleep
from requests import get
from bs4 import BeautifulSoup as bfs

from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class Linkedin():
    """
    Use LinkedIn social media.

    Variables:
        linkedin {str} -- url web page

    """

    linkedin = 'https://www.linkedin.com'

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

        self.chrome.get(self.website + '/login/')

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
            login_buttom = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.CLASS_NAME, 'login__form_action_container')))
            login_buttom.click()
        except TimeoutException as error:
            print('Login buttom not found.', str(error))

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
            me_buttom = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'ember22')))
            me_buttom.click()
        except TimeoutException as error:
            print('User buttom not found.', str(error))

        try:
            out_buttom = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'ember40')))
            out_buttom.click()
        except TimeoutException as error:
            print('Logout buttom not found.', str(error))

        self.chrome.quit()


class Vagas():
    """
    Use Vagas web job plataform.

    Variables:
        vagas {str} -- url web page

    """

    vagas = 'https://www.vagas.com.br'

    def __init__(self, driver, email, password):
        """
        Initialize webdriver.
        """

        self.driver = driver
        self.email = email
        self.password = password
        self.website = Vagas.vagas

        self.chrome = webdriver.Chrome(self.driver)
        self.chrome.wait = WebDriverWait(self.chrome, 3)
        self.chrome.maximize_window()


    def login(self):
        """
        Login on Vagas.
        """

        self.chrome.get(self.website + '/login-candidatos')

        try:
            user_field = WebDriverWait(self.chrome, 3).until(
                presence_of_element_located((By.ID, 'login_candidatos_form_usuario')))

            user_field.send_keys(self.email)
            user_field.send_keys(Keys.TAB)
            sleep(0.5)
        except TimeoutException as error:
            print('Username field not found.', str(error))

        try:
            pw_field = WebDriverWait(self.chrome, 3).until(
                presence_of_element_located((By.ID, 'login_candidatos_form_senha')))

            pw_field.send_keys(self.password)
        except TimeoutException as error:
            print('Password field not found.', str(error))

        try:
            login_buttom = WebDriverWait(self.chrome, 3).until(
                presence_of_element_located((By.ID, 'submitLogin')))

            sleep(0.5)
            login_buttom.submit()
        except TimeoutException as error:
            print('Login buttom not found.', str(error))


    def logout(self):
        """
        Logout from Vagas.
        """

        try:
            candidate_buttom_menu = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.ID, 'menu-candidatos-holder')))
            candidate_buttom_menu.click()
        except TimeoutException as error:
            print('Menu buttom not found.', str(error))

        try:
            out_buttom = WebDriverWait(self.chrome, 5).until(
                presence_of_element_located((By.LINK_TEXT, 'Sair')))
            out_buttom.click()
        except TimeoutException as error:
            print('Logout buttom not found.', str(error))

        self.chrome.quit()


    def search(self, *args):
        """
        Search for job application urls.
        """

        url = self.generate_url(*args)
        self.chrome.get(url)

        while True:
            try:
                more_application = WebDriverWait(self.chrome, 3).until(
                    presence_of_element_located((By.CLASS_NAME, 'btMaisVagas btn')))
                more_application.submit()
            except (TimeoutException, StaleElementReferenceException):
                break

        links = self.extract_links_result(url)
        return links


    def extract_links_result(self, url):
        """
        Gets all job application urls from the html page.
        """

        html = get(url)
        html = html.text

        soup = bfs(html, 'html.parser')
        links = []

        for link in soup.findAll('a', attrs={'href': re.compile("^/vagas/v")}):
            links.append(link.get('href'))
        return links


    def generate_url(self, *args):
        """
        This method create an url serching.

        Parms:
            args -> Some information about the job to create an url.

            Exemple: Job position, city or region, company name.
        """
        info = ''

        for arg in args:
            info = info + '-' + arg

        return self.website + '/vagas-de' + info + '?ordenar_por=mais_recentes'
