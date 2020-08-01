from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class Linkedin():
	""" 
	Use LinkedIn social media.
	"""
	linkedin = 'https://www.linkedin.com/login/'

	def __init__(self, driver, email, password, website=linkedin):
		self.driver = driver
		self.email = email
		self.password = password
		self.website = website

		self.chrome = webdriver.Chrome(self.driver)
		self.chrome.wait = WebDriverWait(self.chrome, 5)
		self.chrome.maximize_window()


	def login(self):
		self.chrome.get(self.website)
		
		try:
			user_field = WebDriverWait(self.chrome, 5).until(
				presence_of_element_located((By.ID, 'username')))

			user_field.send_keys(self.email)
			user_field.send_keys(Keys.TAB)
		except Exception as e:
			print('Username field not found.', str(e))
		
		try:
			pw_field = WebDriverWait(self.chrome, 5).until(
				presence_of_element_located((By.ID, 'password')))

			pw_field.send_keys(self.password)
		except Exception as e:
			print('Password field not found.', str(e))

		try:
			login_button = WebDriverWait(self.chrome, 5).until(
				presence_of_element_located((By.CLASS_NAME, 'login__form_action_container')))
			login_button.click()
		except Exception as e:
			print('Login button not found.', str(e))

		self.minimize_window_msg()


	def minimize_window_msg(self):
		try:
			msg = WebDriverWait(self.chrome, 5).until(
				presence_of_element_located((By.CLASS_NAME, 'msg-overlay-bubble-header')))
			msg.click()
		except Exception as e:
			print('Chat window element not found.', str(e))


	def logout(self):
		try:
			me_button = WebDriverWait(self.chrome, 5).until(
				presence_of_element_located((By.ID, 'ember22')))
			me_button.click()
		except Exception as e:
			print('User button not found.', str(e))

		try:
			out_button = WebDriverWait(self.chrome, 5).until(
				presence_of_element_located((By.ID, 'ember40')))
			out_button.click()
		except Exception as e:
			print('Logout button not found.', str(e))
