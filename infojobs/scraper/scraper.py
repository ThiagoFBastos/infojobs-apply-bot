from bs4 import BeautifulSoup
from utils.selenium import get_by_xpath, get_by_xpath_to_click
import logging

TAG_WAIT_TIME = 5

logger = logging.getLogger(__name__)

def getEmailInputLogin(driver):
    INPUT_EMAIL_XPATH = "//*[@id = 'Email']"
    return get_by_xpath(driver, INPUT_EMAIL_XPATH, TAG_WAIT_TIME)

def getPasswordInputLogin(driver):
    INPUT_PASSWORD_XPATH = "//*[@id = 'Password']"
    return get_by_xpath(driver, INPUT_PASSWORD_XPATH, TAG_WAIT_TIME)

def getButtonLogin(driver):
    BUTTON_XPATH = "//button[@value = 'login']"
    return get_by_xpath_to_click(driver, BUTTON_XPATH, TAG_WAIT_TIME)

def getAlertLogin(driver):
    ALERT_XPATH = "//div[@class = 'alert alert-action mt-15 js_providerLogin']"
    return get_by_xpath(driver, ALERT_XPATH, TAG_WAIT_TIME)

def getAgreeButton(driver):
    AGREE_BUTTON_XPATH = "//*[@id = 'didomi-notice-agree-button']"
    return get_by_xpath_to_click(driver, AGREE_BUTTON_XPATH, TAG_WAIT_TIME)

def getKeywordsInput(driver):
    KEYWORDS_INPUT_XPATH = "//*[@id = 'keywordsCombo']"
    return get_by_xpath(driver, KEYWORDS_INPUT_XPATH, TAG_WAIT_TIME)

def getLocationInput(driver):
    LOCATION_INPUT_XPATH = "//*[@id = 'city']"
    return get_by_xpath(driver, LOCATION_INPUT_XPATH, TAG_WAIT_TIME)

def getButtonSearch(driver):
    DIV_LOCATION_XPATH = "//div[@class = 'job-location-filter-btn']"
    SEARCH_BUTTON_XPATH = './a'
    div_location = get_by_xpath(driver, DIV_LOCATION_XPATH, TAG_WAIT_TIME)
    return get_by_xpath_to_click(div_location, SEARCH_BUTTON_XPATH, TAG_WAIT_TIME)

def getApplyButton(driver):
    APPLY_BUTTON_XPATH = "//a[@class = 'btn btn-primary btn-block js_buttonloading js_btApplyVacancy']"
    return get_by_xpath_to_click(driver, APPLY_BUTTON_XPATH, TAG_WAIT_TIME)

def getLastNavigationPage(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find('ul', attrs = {'class': 'pagination justify-content-center'})
        lis = ul.find_all('li')[-2]
        a = lis.find('a')
        return int(a.get_text())
    except Exception as ex:
        logger.error(f'error when extract last page number: {ex}')

def getJobs(html):
    try:
        urls = []
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all('div', attrs = {'class': 'py-16 pl-24 pr-16 cursor-pointer js_vacancyLoad js_cardLink'})
        for div in divs:
            a = div.find('a', attrs = {'class': 'text-decoration-none'})
            urls.append(a['href'])  
    except Exception as ex:
        logger.error(f'error when extract data from job: {ex}')
    return urls
