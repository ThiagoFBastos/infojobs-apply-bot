import os
import pickle
import logging
import os.path
import requests
import infojobs.filters as filters
import infojobs.scraper as InfoJobsScraper
from time import sleep
from selenium import webdriver
from urllib.parse import urlencode
from selenium.webdriver import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

logger = logging.getLogger(__name__)

class InfoJobs(object):

    def __init__(self, email, password):
        self._urls = {
            'BASE': 'https://www.infojobs.com.br',
            'LOGIN': 'https://login.infojobs.com.br/Account/Login',
            'CANDIDATE': 'https://www.infojobs.com.br/Candidate/'
        }

        self._COOKIES_DIR = 'cookies'

        self._is_logged = False
        self._email = email
        self._password = password

        self.createDriver()

    def createDriver(self):
        if self.is_logged:
            self._driver.quit()

        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        self._driver = webdriver.Firefox(service = FirefoxService(GeckoDriverManager().install()), options = options)

    def _loadCookies(self):
        self._driver.get(self._urls['BASE'])

        if not os.path.isfile(f'{self._COOKIES_DIR}/cookies.pkl'):
            return False

        if not os.path.isfile(f'{self._COOKIES_DIR}/session.pkl'):
            return False

        with open(f'{self._COOKIES_DIR}/session.pkl', 'rb') as f:
            session = pickle.load(f)

        if session['USER_EMAIL'] != self._email or session['USER_PASSWORD'] != self._password:
            self._removeCookies()
            return False

        with open(f'{self._COOKIES_DIR}/cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)

        for cookie in cookies:
            self._driver.add_cookie(cookie)

        self._driver.get(self._urls['CANDIDATE'])

        if self._driver.current_url != self._urls['CANDIDATE']:
            return False

        return True

    def _saveCookies(self):
        self._driver.get(self._urls['BASE'])

        if not os.path.isdir('cookies'):
            os.mkdir('cookies')

        with open(f'{self._COOKIES_DIR}/cookies.pkl', 'wb') as f:
            cookies = self._driver.get_cookies()
            pickle.dump(cookies, f)

        with open(f'{self._COOKIES_DIR}/session.pkl', 'wb') as f:
            session = {'USER_EMAIL': self._email, 'USER_PASSWORD': self._password}
            pickle.dump(session, f)

    def _removeCookies(self):
        cookie_file = f'{self._COOKIES_DIR}/cookies.pkl'
        session_file = f'{self._COOKIES_DIR}/session.pkl'

        if os.path.isfile(cookie_file):
            os.remove(cookie_file)

        if os.path.isfile(session_file):
            os.remove(session_file)

    def login(self):
        WAIT_TIME_LOGIN = 5

        self._is_logged = True

        if self._loadCookies():
            return

        while self._driver.current_url != self._urls['CANDIDATE']:
            try:
                if self._driver.current_url != self._urls['LOGIN']:
                    self._driver.get(self._urls['LOGIN'])        
                    if self._driver.current_url == self._urls['CANDIDATE']:
                        break

                agree_button = InfoJobsScraper.getAgreeButton(self._driver)

                if agree_button is not None:
                    agree_button.click()

                input_email = InfoJobsScraper.getEmailInputLogin(self._driver)

                input_email.send_keys(self._email)
        
                button = InfoJobsScraper.getButtonLogin(self._driver)

                button.click()

                alert = InfoJobsScraper.getAlertLogin(self._driver)

                if alert is not None:
                    button.click()

                input_password = InfoJobsScraper.getPasswordInputLogin(self._driver)

                input_password.send_keys(self._password)

                input_password.send_keys(Keys.ENTER)

                sleep(WAIT_TIME_LOGIN)
            except Exception as ex:
                logger.error(f'error when try login: {ex}')
                self._driver.refresh()

        self._saveCookies()

    def quit(self):
        self._driver.quit()
        self._is_logged = False

    @property
    def is_logged(self):
        return self._is_logged

    def apply(self, url):
        try:
            self._driver.get(url)
            button = InfoJobsScraper.getApplyButton(self._driver)
            button.click()
            return True
        except Exception as ex:
            logger.error(f'error when apply for job: {ex}')
        return False

    def search_jobs(self, keywords, city = None, state = None, limit = -1, workplaceType = None, publicationTime = None, salary = None, profissionalArea = None, contract = None, journey = None, pwd = None):
        
        if city: city = city.replace(' ', '-')

        page = 1
        posts = []

        while limit == -1 or len(posts) < limit:

            params = {
                'palabra': keywords,
                'page': page
            }

            if workplaceType:
                params['idw'] = filters.WorkPlaceType[workplaceType]

            if publicationTime:
                params['Antiguedad'] = filters.PublicationTime[publicationTime]

            if salary:
                params['isr'] = filters.Salary[salary]

            if profissionalArea:
                params['categoria'] = ','.join(map(str, [filters.ProfissionalArea[p] for p in profissionalArea]))

            if journey:
                params['wo'] = ','.join(map(str, [filters.Journey[j] for j in journey]))

            if pwd:
                params['def1'] = ','.join(map(str, [filters.Pwd[p] for p in pwd]))

            if contract:
                params['tipocontrato'] = ','.join(map(str, [filters.Contract[c] for c in contract]))

            if city:
                URL = f"{self._urls['BASE']}/vagas-de-emprego-em-" + '{}.aspx?' + urlencode(params)
                location = f'{city},-{state}' if state else city
                URL = URL.format(location)
            else:
                URL = f"{self._urls['BASE']}/empregos.aspx?{urlencode(params)}"

            page_source = requests.get(URL).content

            results = InfoJobsScraper.getJobs(page_source)

            results = list(map(lambda href: f"{self._urls['BASE']}{href}", results))

            posts.extend(results)

            if page == InfoJobsScraper.getLastNavigationPage(page_source):
                break

            page += 1

        if limit == -1:
            return posts

        return posts[:limit]
