from src.driver import DriverPreparation
from src.services import Linkedin, Vagas

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


def credentials(service):
	""" 
	Returns login credentials.
	"""

	with open('C:/Users/mekyl/OneDrive/Documentos/chave.key', 'rb') as k:
		key = k.read()

	with open('./src/credentials_' + service + '.txt', 'r') as c:
		lines = c.readlines()

	f = Fernet(key)

	return [f.decrypt(line.encode()).decode() for line in lines]


def use_linkedin(driver, email, password):
	"""
	Run LinkedIn process.
	"""

	linkedin = Linkedin(driver, email, password)
	linkedin.login()
	linkedin.logout()


def use_vagas(driver, email, password):
	"""
	Run Vagas process.
	"""

	vagas = Vagas(driver, email, password)
	vagas.login()
	vagas.logout()


def main(service='vagas'):
	"""
	Main function.
	
	"""

	driver = set_driver()
	email, password = [*credentials(service)]

	if service.lower().strip() == 'linkedin':
		return use_linkedin(driver, email, password)
	else:
		return use_vagas(driver, email, password)


if __name__ == '__main__':
	main()
