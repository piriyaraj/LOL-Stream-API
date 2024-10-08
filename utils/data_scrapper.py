from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

class DataScrapper:
    def __init__(self, headless=False) -> None:
        self.__options = Options()
        if headless:
            self.__options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=self.__options)



    def quit(self):
        self.driver.quit()