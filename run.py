""" Modules import """
from cryptography.fernet import Fernet

from src.driver import DriverPreparation
from src.services import Linkedin, Vagas



def set_driver():
    """
    Returns url path from webdriver directory.

    """

    driver = DriverPreparation()

    chrome_driver = driver.chrome_driver()

    return chrome_driver


def credentials(service):
    """
    Returns login credentials.

    """

    with open('C:/Users/mekyl/OneDrive/Documentos/chave.key', 'rb') as key_file:
        key = key_file.read()

    with open('./src/credentials_' + service + '.txt', 'r') as credentials_file:
        lines = credentials_file.readlines()

    fernet = Fernet(key)

    return [fernet.decrypt(line.encode()).decode() for line in lines]


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
    links = vagas.search('supervisor')
    print(links)
    print(len(links))
    #vagas.logout()
    input()


def main(service='vagas'):
    """
    Main function.

    """

    driver = set_driver()
    email, password = [*credentials(service)]

    if service.lower().strip() == 'linkedin':
        return use_linkedin(driver, email, password)
    return use_vagas(driver, email, password)


if __name__ == '__main__':
    main()
