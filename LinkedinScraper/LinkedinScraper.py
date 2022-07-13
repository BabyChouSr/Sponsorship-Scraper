#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# script.py

import parameters
import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
import os
import sys
import clearbit
import random
from tldextract import extract
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
# from fp.fp import FreeProxy
# from fake_useragent import UserAgent

FILE_NAME = '../data/recruiters.csv'
FIELDS = ['Name', 'Job Title', 'Link', 'Domain Name']
clearbit.key = parameters.clearbit_key
driver = webdriver.Chrome(ChromeDriverManager().install())


'''
TODO(chris): add spoofing dw about it!!

Currently being developed
class Spoofer(object):

    def __init__(self, country_id=['US'], rand=True, anonym=True):
        self.country_id = country_id
        self.rand = rand
        self.anonym = anonym
        self.userAgent, self.ip = self.get()

    def get(self):
        ua = UserAgent()
        proxy = FreeProxy(country_id=self.country_id, rand=self.rand, anonym=self.anonym).get()
        ip = proxy.split("://")[1]
        return ua.random, ip


class DriverOptions(object):

    def __init__(self):

        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--incognito")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("disable-infobars")

        self.helperSpoofer = Spoofer()

        self.options.add_argument('user-agent={}'.format(self.helperSpoofer.userAgent))
        self.options.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)


class WebDriver(DriverOptions):

    def __init__(self, path=''):
        DriverOptions.__init__(self)
        self.driver_instance = self.get_driver()

    def get_driver(self):

        print("""
        IP:{}
        UserAgent: {}
        """.format(self.helperSpoofer.ip, self.helperSpoofer.userAgent))

        PROXY = self.helperSpoofer.ip
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":PROXY,
            "ftpProxy":PROXY,
            "sslProxy":PROXY,
            "noProxy":None,
            "proxyType":"MANUAL",
            "autodetect":False
        }
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

        path = os.path.join(os.getcwd(), '../windowsDriver/chromedriver.exe')

        driver = webdriver.Chrome(executable_path = ChromeDriverManager().install(), options=self.options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })

        return driver
    driver = WebDriver()
'''

# function to ensure all key data fields have a value
def validate_field(field):
    if field == 'None':
        field = 'No results'
        return field
    else:
        return field

### REGION --- RUN SCRIPT TO GET LINKEDIN PROFILES
def getLinkedinProfiles():
    print("Searching for these companies:", parameters.companies)
    for company in parameters.companies:
        company_search = f'site:linkedin.com/in/ AND {company} AND technical recruiter'
        domain_name =  clearbit.NameToDomain.find(name=company)['domain']
        driver.get('https://www.google.com')
        sleep(2)
        search_query = driver.find_element(By.NAME,'q')
        search_query.send_keys(company_search)
        sleep(0.5)

        search_query.send_keys(Keys.RETURN)
        sleep(3)

        # Get list of all linkeding profile URLs
        elems = driver.find_elements(By.XPATH,"//a[@href]")

        #let's limit to 5 links each
        linkedin_urls = []
        count = 0
        for elem in elems:
            if not 'google' in elem.get_attribute("href") and 'linkedin' in elem.get_attribute("href") and count < 5:
                linkedin_urls.append(elem.get_attribute("href"))
                count += 1
        linkedin_urls
        sleep(0.5)

        with open(FILE_NAME, 'a') as f:
            csv_writer = csv.writer(f)
            if os.stat(FILE_NAME).st_size == 0:
                csv_writer.writerow(FIELDS) # write header

        # For loop to iterate over each URL in the list
            for linkedin_url in linkedin_urls:
                # open profile URL
                driver.get(linkedin_url)

                # add a 3 second pause loading each URL
                sleep(3)

                # assigning the source code for the webpage to variable sel
                sel = Selector(text=driver.page_source)

                name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
                if name:
                    name = name.strip()
                    # print(name)

                job_title = sel.xpath('//*[starts-with(@class, "text-body-medium break-words")]/text()').extract_first()
                if job_title:
                    job_title = job_title.strip()
                    # print(jobtitle)

                location = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()
                if location:
                    location = location.strip()
                    # print(location)

                # currentJob = sel.xpath('//h3/text()').extract_first()

                linkedin_url = driver.current_url

                # validating if the fields exist on the profile
                name = validate_field(name)
                job_title = validate_field(job_title)
                # location = validate_field(location)
                linkedin_url = validate_field(linkedin_url)

                # Print what information is being write to the CSV file
                rows = [name,job_title,linkedin_url, domain_name]
                print('Writing to CSV:', rows)

                # Write ROW content to the CSV file
                csv_writer.writerow(rows)
                sleep(random.random() * 10) # add a random delay to avoid bot detection

### REGION ------ BEGIN PERMUTING EMAILS
def getHostName(website):
    tsd, td, tsu = extract(website)
    url = td + '.' + tsu
    return url

#test permuted emails package
def nameToEmail(first_name, last_name, domain_name):
	listOfPossibleEndings = ['.com', '.net', '.io']

	# 3 of the most popular sequences:
	# {first}.{last}
	# {f}{last}
	# {first}{last}
	permuted_emails = [
		first_name + '.' + last_name + '@' + domain_name,
		first_name + last_name + '@' + domain_name,
		first_name[0] + last_name + '@' + domain_name,
	]

	# join permuted_emails together into string separated by comma
	permuted_emails = ','.join(permuted_emails)
	return permuted_emails


def permuteEmails():
    df = pd.read_csv(FILE_NAME)
    df = df[['Name', 'Domain Name']]

    ### CLEAN UP DATA
    df[['First Name', 'Last Name']] = df['Name'].loc[df['Name'].str.split().str.len() == 2].str.split(expand=True)
    df['Domain Name'] = df['Domain Name'].apply(lambda x: getHostName(x))
    df['First Name'].fillna(df['Name'],inplace=True)
    df['First Name'].fillna("",inplace=True)
    df['Last Name'].fillna("",inplace=True)

    # clean our first name, last name. and company columns
    df['First Name'] = df['First Name'].str.strip()
    df['First Name'] = df['First Name'].str.lower()
    df['First Name'] = df['First Name'].str.replace('.','')
    df['Last Name'] = df['Last Name'].str.lower()
    df['Last Name'] = df['Last Name'].str.strip()
    df['Last Name'] = df['Last Name'].str.replace('.','')

    # drop empty last name rows
    df = df[df['Last Name'] != '']
    #drop empty first name rows
    df = df[df['First Name'] != '']

    # map the nameToEmail function across the dataframe df
    for i in df.index:
        df.loc[i, 'Email'] = nameToEmail(df.loc[i, 'First Name'], df.loc[i, 'Last Name'], df.loc[i, 'Domain Name'])

    df = df.set_index(['Name', 'Domain Name', 'First Name', 'Last Name']).apply(lambda x: x.str.split(',').explode()).reset_index()
    df.reset_index(drop=True, inplace=True)
    df.to_csv('../out/permutedEmailsResult.csv')


### REGION --- MAIN SCRIPT
def main():
    # install chromedrive when needed
    print("FINISHED INSTALLING DRIVER")

    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com/login')

    # locate email form by element_by_id
    username = driver.find_element(By.ID,'username')
    # use data from Parameters file imported vars
    username.send_keys(parameters.linkedin_username)

    # locate email form by element_by_id
    password = driver.find_element(By.ID,'password')
    # use data from Parameters file imported vars
    password.send_keys(parameters.linkedin_password)

    # locate submit button by_class_name
    log_in_button = driver.find_element(By.CLASS_NAME, 'btn__primary--large')

    # locate submit button by_xpath
    log_in_button = driver.find_element(By.XPATH,'//*[@type="submit"]')

    # .click() to mimic button click
    log_in_button.click()
    sleep(0.5)
    print("LOGGED IN")
    getLinkedinProfiles()
    print("==== FINISHED EXTRACTING ALL COMPANIES ==== ")
    permuteEmails()

if __name__ == "__main__":
    main()