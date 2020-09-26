from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from Main.models import Bots
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

os.environ['email'] = 'abcd@gmail.com'
os.environ['password'] = 'abcd'

email = os.environ['email']
password = os.environ['password']
# os.environ['CHROMEDRIVER_PATH'] = r'C:\Users\Darshan\Desktop\chromedriver_win32\chromedriver'


def report():
    print("started")
    options = webdriver.ChromeOptions()
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"),options=options)
    browser.get('http://www.instagram.com')

    email = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input')))

    password = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label/input')))

    email.send_keys(email)
    password.send_keys(password)
    button = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
    button.click()
    browser.implicitly_wait(5)
    try:
        browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    except:
        pass

    bot_usernames = Bots.objects.values_list('username', flat=True)

    for username in bot_usernames[:3]:
        input_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
        input_box.send_keys(username)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]'))).click()

        browser.implicitly_wait(5)
        for _ in range(3):
            try:
                three_dot = browser.find_element_by_class_name('wpO6b ')
                three_dot.click()
                break
            except:
                pass

        report_btn = browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/button[3]')
        report_btn.click()
        browser.implicitly_wait(5)
        spam_btn = browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div/div/div[3]/button[1]')
        spam_btn.click()
        pop_up = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div/div/div/div[2]/button")))
        pop_up.click()
        browser.implicitly_wait(2)
        print(f"{username} reported")
        Bots.objects.get(username=username).delete()
        time.sleep(5)

    browser.quit()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(),"default")
    scheduler.add_job(report,'interval',minutes=1, name='report_accounts',jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler has started")