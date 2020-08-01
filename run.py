from src.driver import DriverPreparation
from src.services import Linkedin

from cryptography.fernet import Fernet


def set_driver():
	"""
	Returns url path from webdriver directory.
	
	"""

	dp = DriverPreparation()

	chrome_driver = dp.chrome_driver()

	if not chrome_driver == None:
		return chrome_driver
	else:
		dp.update_driver()
		chrome_driver = dp.chrome_driver()
		return chrome_driver


def credentials():
	""" 
	Returns login credentials.
	"""

	with open('C:/Users/mekyl/OneDrive/Documentos/chave.key', 'rb') as k:
		key = k.read()

	with open('./src/credentials.txt', 'r') as c:
		lines = c.readlines()

	f = Fernet(key)

	return [f.decrypt(line.encode()).decode() for line in lines]



driver = set_driver()
email, password = [*credentials()]

linkedin = Linkedin(driver, email, password)
linkedin.login()
linkedin.logout()



