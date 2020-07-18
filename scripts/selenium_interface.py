from selenium import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

class Driver:
    def __init__(self, url):
        self.url    = url
        self.driver = None

    # Function : get_script
    # Purpose  : get html page given url from driver
    # Input    : url
    def get_script(self, url):
        if url is None:
            self.driver.get(self.url)
        else:
            self.driver.get(url)
        page = self.driver.execute_script("return document.body.innerHTML").encode('utf-8')
        if page is not None:
            print("GOT SCRIPT!!")
        return page
    
    # Function : kill
    # Purpose  : close and quit driver
    def kill(self):
        self.driver.close()
        self.driver.quit()

# Class   : ChromeDriver
# Purpose : given a certain url, construct a new Chrome Driver object
# Input   : url
class ChromeDriver(Driver):
    def __init__(self, url):
        try:
            self.url    = url
            self.driver = None

            software_names     = [SoftwareName.CHROME.value]
            operating_systems  = [OperatingSystem.WINDOWS.value,
                                  OperatingSystem.LINUX.value]
            user_agent_rotator = UserAgent(software_names=software_names,
                                          operating_systems=operating_systems,
                                          limit=100)
            user_agent         = user_agent_rotator.get_random_user_agent()
            prefs              = {'profile.managed_default_content_settings.images':2}
            options            = webdriver.ChromeOptions()

            options.add_argument("user-agent={user_agent}")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_experimental_option("prefs", prefs)

            TedPath = '/home/devadmin/Desktop/chromedriver'
            SamPath = '/Users/sam/Desktop/chromedriver'
            self.driver = webdriver.Chrome(executable_path=TedPath, chrome_options=options)
            if self.url is not None:
                self.driver.get(self.url)
        except:
            print("ERROR: CHROME DRIVER")

    # Function : extract
    # Purpose  : Given a url and path, extract data from the built selenium driver.
    # Input    : url, path
    def extract(self, url, path):
        if url is not None:
            if url is not self.url:
                self.url = url
        self.driver.get(self.url)
        target = ""
        try:
            target = (self.driver.find_elements_by_xpath(path)[0]).text
        except:
            print("ERROR: LINK CHASE on URL: " + str(url) + " WITH PATH: " + path)
            pass
        return target

    def get_script(self, url):
        return super().get_script(url)

    def kill(self):
        return super().kill()

# Class   : FireDriver
# Purpose : given a certain url, construct a new Firefox Driver object
# Input   : url
class FireDriver(Driver):
    def __init__(self, url):
        self.url    = url
        self.driver = None
        try:
            opts = Options()
            opts.headless = True
            self.driver = webdriver.Firefox(options=opts)
            if self.url is not None:
                self.driver.get(self.url)
        except:
            print("ERROR: FIREDRIVER")
    
    def get_script(self, url):
        return super().get_script(url)
    
    def kill(self):
        return super().kill()