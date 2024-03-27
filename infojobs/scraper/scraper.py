from bs4 import BeautifulSoup
from utils.selenium import get_by_xpath, get_by_xpath_to_click
import re

TAG_WAIT_TIME = 5

def getEmailInputLogin(driver):
    try:
        INPUT_EMAIL_XPATH = "//*[@id = 'Email']"
        return get_by_xpath(driver, INPUT_EMAIL_XPATH, TAG_WAIT_TIME)
    except:
        raise RuntimeError('Tag not found in getEmailInputLogin method')

def getPasswordInputLogin(driver):
    try:
        INPUT_PASSWORD_XPATH = "//*[@id = 'Password']"
        return get_by_xpath(driver, INPUT_PASSWORD_XPATH, TAG_WAIT_TIME)
    except:
        raise RuntimeError('Tag not found in getPasswordInputLogin method')

def getButtonLogin(driver):
    try:
        BUTTON_XPATH = "//button[@value = 'login']"
        return get_by_xpath_to_click(driver, BUTTON_XPATH, TAG_WAIT_TIME)
    except:
        raise RuntimeError('Tag not found in getButtonLogin method')

def getAlertLogin(driver):
    try:
        ALERT_XPATH = "//div[@class = 'alert alert-action mt-15 js_providerLogin']"
        return get_by_xpath(driver, ALERT_XPATH, TAG_WAIT_TIME)
    except:
        raise RuntimeError('Tag not found in getAlertLogin method')

def getAgreeButton(driver):
    try:
        AGREE_BUTTON_XPATH = "//*[@id = 'didomi-notice-agree-button']"
        return get_by_xpath_to_click(driver, AGREE_BUTTON_XPATH, TAG_WAIT_TIME)
    except:
        raise RuntimeError('Tag not found in getAgreeButton method')

def getApplyButton(driver):
    try:
        APPLY_BUTTON_XPATH = "//a[@class = 'btn btn-primary btn-block js_buttonloading js_btApplyVacancy']"
        return get_by_xpath_to_click(driver, APPLY_BUTTON_XPATH, TAG_WAIT_TIME)
    except:
        raise RuntimeError('Tag not found in getApplyButton method')

def getLastNavigationPage(html):
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', attrs = {'class': 'pagination justify-content-center'})
    if ul is None:
        raise RuntimeError('Tag not found in getLastNavigationPage method')
    lis = ul.find_all('li')
    if len(lis) < 2:
        raise RuntimeError('Tag not found in getLastNavigationPage method')
    lis = lis[-2]
    a = lis.find('a')
    if a is None:
        raise RuntimeError('Tag not found in getLastNavigationPage method')
    if not re.match(r'^\d+$', a.get_text()):
        raise RuntimeError('Tag doesn\'t contains integer')
    return int(a.get_text())

def getJobs(html):
    urls = []
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', attrs = {'class': 'py-16 pl-24 pr-16 cursor-pointer js_vacancyLoad js_cardLink'})
    for div in divs:
        a = div.find('a', attrs = {'class': 'text-decoration-none'})
        if a is None:
            raise RuntimeError('Tag not found inf getJobs method')
        elif 'href' in a.attrs:
            urls.append(a['href'])
    return urls
