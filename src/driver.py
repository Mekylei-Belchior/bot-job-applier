""" Modules import """
from os import listdir, path, mkdir
from os.path import isdir
from shutil import rmtree

from zipfile import ZipFile, is_zipfile
from io import BytesIO

from requests import get as download
from bs4 import BeautifulSoup as bfs


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


    def __check_path(self, d_path):
        """
        Verify the directory of the path argument.

        """

        if path.exists(d_path):
            path_names = [d for d in listdir(d_path) if isdir(d_path + '/' + d)]

            if len(path_names) > 0:
                return path_names
            return None
        return False


    def chrome_driver(self):
        """
        Returns the chrome driver path.

        """
        driver = self.driver_version()
        return self.driver + driver + '/chromedriver'


    def driver_version(self):
        """
        Check webdriver version.
        """
        return self.__get_driver_version(self.driver)


    def __get_driver_version(self, d_path):
        """
        Returns the driver version.

        """

        items = self.__check_path(d_path)

        if items is False:
            mkdir(self.driver)
        elif items is None:
            return self.__download_file()
        else:
            for item in items:
                if item.replace('.', '').isdigit() and len(item) > 11:
                    return item

        return self.__download_file()


    def chrome_version(self):
        """
        Check chrome browser version.
        """
        version = self.__get_chrome_version(self.chrome)

        if not version is None:
            return version
        return 'Chrome version not found.'


    def __get_chrome_version(self, d_path):
        """
        Returns the version of web browser Chrome if it is found.

        """

        items = self.__check_path(d_path)

        if not items:
            return None

        for item in items:
            if item.replace('.', '').isdigit() and len(item) > 11:
                return item


    def update_driver(self):
        """
        This method update chrome webdriver if webdriver version is lower
        than chrome version.

        """
        confirm = self.__check_update()

        if confirm:
            version = self.__download_file()
            return version


    def __check_update(self):
        """
        Check chrome browser and webdriver version.

        """

        driver_version = self.driver_version()
        chrome_version = self.chrome_version()
        objects = [driver_version, chrome_version]

        items = []

        if all(objects):
            for item in objects:
                items.append(item.replace('.', '').isdigit())

            if all(items):
                if driver_version < chrome_version:
                    return True
                return False
        return True


    def __link_download(self):
        """
        Generates download link for the last chrome webdriver stable release.

        """

        html = download(self.page)
        html = html.text

        soup = bfs(html, 'html.parser')
        tag = soup.select(
            '#sites-canvas-main-content>table>tbody>tr>td>div>div:nth-child(5)>ul>li:nth-child(1)>a'
        )

        stable_release = list(tag[0])
        stable_release = stable_release[0][13:]

        return self.link.replace('*', stable_release), stable_release


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
                if all([folders is not None, folders is not False]):
                    for folder in folders:
                        rmtree(self.driver + folder)
            except Exception as error:
                print('Could not delete driver folder.', str(error))

            try:
                # Create a new driver directory
                mkdir(self.driver + release)
                # Unzip the file
                file.extractall(self.driver + release)
                return release
            except Exception as error:
                print('Could not salve the file.', str(error))
        else:
            print('Could not find a zip file.')
