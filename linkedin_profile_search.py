import csv
import sys
import fileinput
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import parameters
from parsel import Selector
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

writer = csv.writer(open(parameters.result_file, 'w'))
writer.writerow(['Sl. No.', 'Name of the Candidate', 'Job Title', 'Schooling/Education', 'Current Location',
                 'Profile LinkedIn URL'])

driver = webdriver.Chrome(r'C:\Users\VISHAL\Downloads\chromedriver_win32\chromedriver.exe')
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(2)
driver.find_element(By.XPATH,'//button[@class="sign-in-form__submit-button"]').click()
sleep(3)
username = driver.find_element(By.NAME,'session_key')
username.send_keys(parameters.user)
sleep(0.5)
password = driver.find_element(By.NAME,'session_password')
password.send_keys(parameters.passw)
sleep(0.5)
driver.find_element(By.XPATH,'//button[@class="sign-in-form__submit-button"]').click()
sleep(5)
driver.get('https://www.google.com/')
sleep(2)
search_input = driver.find_element(By.NAME,'q')

beg = 'site:linkedin.com/in -intitle:profiles -inurl:"/dir'
print('Instructions:')
print('Enter the Keywords you require one by one and then Press Enter')
print('Enter -1 if you are done with your keywords')
for line in sys.stdin:
    if ('-1' == line.rstrip()):
        break
    r1 = line.rstrip()
    beg = beg + ' AND '
    beg = beg + '"{}"'.format(r1)
    print('Enter the next keyword')
    print('Enter -1 if you are done with your keywords')

k = int(input('Enter the number of Profiles Required (between 1 to 200)'))
print('FINDING SUITABLE PROFILES.......')
search_input.send_keys(beg)
sleep(0.5)
search_input.send_keys(Keys.RETURN)
sleep(3)
i = 0
prev = driver.current_url

while i < k:
    profiles = driver.find_elements(By.XPATH,'//*[@class="r"]/a[1]')
    profiles = [profile.get_attribute('href') for profile in profiles]
    for profile in profiles:
        i = i + 1
        driver.get(profile)
        sleep(3)
        linkedin_url = driver.current_url
        if linkedin_url.find('unavailable') != -1:
            i = i - 1
            continue
        if linkedin_url.find('linkedin') == -1:
            i = i - 1
            continue

        sel = Selector(text=driver.page_source)
        name = sel.xpath('//title/text()').extract_first().split(' | ')[0].strip()
        if name[0] == '(':
            name = name.split(')')[1].strip()
        print(i)
        print('Scraping Profile of ' + name)
        temp = sel.xpath('//h2/text()').extract()
        sz = len(temp)
        job_title = '';

        if sz >= 2:
            job_title = temp[1].strip()
        else:
            job_title = temp[0].strip()

        schools = sel.xpath('//*[contains(@class,"pv-entity__school-name")]/text()').extract()
        location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
        try:
            writer.writerow([i, name, job_title, schools, location, linkedin_url])
        except:
            continue
        if i == k:
            break
    if i == k:
        break

    driver.get(prev)
    sleep(2)
    clicker = driver.find_elements(By .XPATH,'//span[text()="Next"]')
    if len(clicker) > 0:
        clicker[0].click()
        sleep(2)
    else:
        print('Number of profiles Does Not meet User Requirements')
        break;

    prev = driver.current_url

driver.quit()