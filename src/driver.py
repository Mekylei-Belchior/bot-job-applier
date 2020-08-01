from os import listdir, path, mkdir
from os.path import isdir
from shutil import rmtree

from zipfile import ZipFile, is_zipfile
from io import BytesIO

from requests import get		as download
from bs4 import BeautifulSoup	as bfs


class DriverPreparation():
	"""
	Get ready chrome webdriver to use in Selenium.

	Variables:
		p {str} -- Chrome Webdriver page
		l {str} -- URL to Google API directory
		c {str} -- Chrome Web Browser directory path
		d {str} -- Webdriver path

	"""

	p = 'https://chromedriver.chromium.org/'
	l = 'https://chromedriver.storage.googleapis.com/*/chromedriver_win32.zip'
	c = 'C:/Program Files (x86)/Google/Chrome/Application'
	d = './driver/'

	def __init__(self, driver=d, chrome=c, link=l, page=p):
		self.driver = driver
		self.chrome = chrome
		self.link = link
		self.page = page	


	def __check_path(self, dPath):
		"""
		Returns directory path names or None if nothing is found.

		"""

		if path.exists(dPath):
			path_names = [d for d in listdir(dPath) if isdir(dPath + '/' + d)]
			return path_names if len(path_names) > 0 else None
		else:
			return None


	def chrome_driver(self):
		"""
		Returns the chrome driver path to use.
		
		"""

		dp = self.__check_path(self.driver)
		
		confirm = all([not dp is None, len(dp[0]) > 11])

		if confirm:
			return self.driver + self.driver_version() + '/chromedriver'
		else:
			return None



	def __get_version(self, dPath):
		"""
		Returns the version of the object if it is found.
		
		"""

		items = self.__check_path(dPath)
		
		if not items is None:
			for item in items:
				if item.replace('.', '').isdigit() and len(item) > 11:
					return item
				else:
					return None	
		else:
			return None


	def chrome_version(self):
		"""
		Check chrome browser version.
		"""
		version = self.__get_version(self.chrome)
		
		if not version == None:
			return version
		else:
			return 'Chrome version not found.'


	def driver_version(self):
		"""
		Check webdriver version.
		"""
		version = self.__get_version(self.driver)
		
		if not version == None:
			return version
		else:
			return 'Webdriver version not found.'


	def __check_update(self):
		"""
		Check chrome browser and webdriver version.
		
		"""

		driverVersion = self.__get_version(self.driver)
		chromeVersion = self.__get_version(self.chrome)
		objects = [driverVersion, chromeVersion]
		
		items = []

		if all(objects):
			for item in objects:
				items.append(item.replace('.', '').isdigit())
			
			if all(items):
				return True if driverVersion < chromeVersion else False
			else:
				return None
		else:
			return True


	def __link_download(self):
		"""
		Generates download link for the last chrome webdriver stable release.
		
		"""
		
		html = download(self.page)
		html = html.text

		soup = bfs(html, 'html.parser')
		tag = soup.select('#sites-canvas-main-content > table > tbody > tr > td > div > div:nth-child(5) > ul > li:nth-child(1) > a')
		stable_release = list(tag[0])
		stable_release = stable_release[0][13:]

		return self.link.replace('*', stable_release), stable_release


	def update_driver(self):
		"""
		This method update chrome webdriver whether webdriver version is lower
		than chrome version.

		"""

		check = self.__check_update()

		if check:
			self.__download_file()


	def __download_file(self):
		"""
		Download chrome webdriver.
		"""

		url, release = self.__link_download()

		content = download(url, stream=True)
		iszip = is_zipfile(BytesIO(content.content))

		if iszip:
			file = ZipFile(BytesIO(content.content))

			try:
				folders = self.__check_path(self.driver)

				# Delete each folder in driver directory
				if not folders is None and len(folders) > 0:
					for folder in folders:
						rmtree(self.driver + folder)
			except Exception as e:
				print('Could not delete driver folder.', str(e))

			try:
				# Create a new driver directory
				mkdir(self.driver + release)
				# Unzip the file
				with file as f:
					f.extractall(self.driver + release)

			except Exception as e:
				print('Could not salve the file.', str(e))
		else:
			print('Could not find a zip file.')
