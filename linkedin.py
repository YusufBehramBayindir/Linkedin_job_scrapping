import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 170)


#Import Packages

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# url1=("https://www.linkedin.com/jobs/search/?currentJobId=3573877291&f_AL=true&f_TPR=r604800&f_WT=2&geoId=105080838&keywords=data%20scientist&location=New%20York%2C%20United%20States&refresh=true&sortBy=R")
# url2 = ("https://www.linkedin.com/jobs/search/?currentJobId=3573877291&f_AL=true&f_I=14%2C6%2C84%2C96%2C42&f_T=30006%2C340%2C2732&f_WT=2%2C3&geoId=105080838&keywords=data%20scientist&location=New%20York%2C%20United%20States&refresh=true&sortBy=R")

url1 = input("LinkedIn iş ilanı sayfasının URL'sini girin: ")
driver = webdriver.Chrome("driver path location")
driver.implicitly_wait(10)
driver.get(url1)

y = driver.find_elements(By.CLASS_NAME, 'results-context-header__job-count')[0].text

type(y)

n = pd.to_numeric(y)

n

i = 2
while i <= int((n + 200) / 25) + 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i = i + 1

    try:
        send = driver.find_element_by_xpath("//button[@aria-label='Load more results']")
        driver.execute_script("arguments[0].click();", send)
        time.sleep(3)

        # buu=driver.find_elements_by_tag_name("button")
        # x=[btn for btn in buu if btn.text=="See more jobs"]
        # for btn in x:
        # driver.execute_script("arguments[0].click();", btn)
        # time.sleep(3)



    except:
        pass
        time.sleep(5)


#Create empty lists for company name and job title

companyname= []
titlename= []

try:
    for i in range(n):
        company = driver.find_elements(By.CLASS_NAME,'base-search-card__subtitle')[i].text
        companyname.append(company)

except IndexError:
    print("no")

len(companyname)

try:
    for i in range(n):
        title = driver.find_elements(By.CLASS_NAME,'base-search-card__title')[i].text

        titlename.append(title)

except IndexError:
    print("no")

len(titlename)

companyfinal = pd.DataFrame(companyname, columns=["Company"])
titlefinal = pd.DataFrame(titlename, columns=["Title"])

x = companyfinal.join(titlefinal)

x.reset_index()
x.head()

x.to_csv('linkedin.csv')

jobList = driver.find_elements(By.CLASS_NAME,'base-card__full-link')
hrefList = []
for e in jobList:
    hrefList.append(e.get_attribute('href'))

# for href in hrefList:
# link.append(href)

hrefList

linklist = pd.DataFrame(hrefList, columns=["joblinks"])

x = x.join(linklist)

x.head()

x.to_csv('linkedin.csv')

#Close the driver
driver.close()


