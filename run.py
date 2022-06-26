from time import sleep
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as tunggu
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager as CM

opt = Options()

# opt.headless = True # uncomment this line if you don't want to show chromewebdriver

opt.add_argument('log-level=3')
opt.add_argument('--ignore-ssl-errors=yes')
opt.add_argument('--ignore-certificate-errors')
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
mobile_emulation = {"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
opt.add_experimental_option("mobileEmulation", mobile_emulation)

dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

def scrape_ig(username, password, target, count):

    open('result.txt', 'w+')

    driver = webdriver.Chrome(options=opt, desired_capabilities=dc, executable_path=CM().install())
    driver.set_window_size(600, 1000)
    driver.get('https://www.instagram.com/accounts/login/')
    # driver.minimize_window()


    print(f"[{time.strftime('%d-%m-%y')}] - LOGIN....")
    tunggu(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))).send_keys(username)
    tunggu(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(password)
    tunggu(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(Keys.ENTER)

    sleep(5)
    print(f"[{time.strftime('%d-%m-%y')}] - SUCCESSFUL LOGIN AT {time.strftime('%H:%M')}")

    sleep(5)
    print(f"\n[{time.strftime('%d-%m-%y')}] - OPENING A @{target} ACCOUNT PROFILE")
    driver.get(f'https://www.instagram.com/{target}/')
    flw = tunggu(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/ul/li[2]/a/div/span')))

    users = set()

    if flw.text[-1::] == "M":
        print(f"[{time.strftime('%d-%m-%y')}] - OPENING A @{target} ACCOUNT FOLLOWERS")
        flw.click()
        sleep(5)
        print("\n[INFO] - START SCRAPING FOLLOWERS...\n")


        for _ in range(round(count // 10)):

            sleep(1)
            ActionChains(driver).send_keys(Keys.END).perform()

            tunggu(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')))
            cekFlw = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')

            for i in cekFlw:
                if i.get_attribute('href'):
                    users.add(i.get_attribute('href').split("/")[3])
                else:
                    continue

    else:
        print("LITTLE TARGET FOLLOWERS, PLEASE FIND OTHER TARGETS")

    print('[INFO] - SAVING RESULT...')

    with open('result.txt', 'r+') as file:
        file.write('\n'.join(users) + "\n")

    print('[DONE] - YOUR RESULT ARE SAVED IN result.txt FILE!')



if __name__ == '__main__':
    username = input("USERNAME =>> ")
    password = input("PASSWORD =>> ")
    target = input("TARGET USERNAME =>> ")
    count = int(input('''COUNT
SUGGESTION: USE NUMBERS FROM 10 - 100 TO INPUT COUNT
=>> '''))

    scrape_ig(username, password, target, count)