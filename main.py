#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
"""
Created on Tusday Oct 8 11:54:42 2020

@author: Najmi Imad
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv

username = "netaporter"

fc_username = "*****" # username of <Facebook Account>
fc_password = "*****" # password of <Facebook Account>

url = "https://www.instagram.com/{}/".format(username)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
chrome_options.add_argument('--enable-automation')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.headless=False

driver = webdriver.Chrome("../chromedriver", chrome_options=chrome_options)

#go to profile
driver.get(url)

sleep(9)
# clcick on followers link
driver.find_element_by_css_selector('a.-nal3').click()
# wait for the login form dialog
sleep(3)

#click on connect with Facbook button 
wait = WebDriverWait(driver, 10)
btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.KPnG0')))
btn.click()

# wait for redirection
sleep(2)

# fill in and submit the form
driver.find_element_by_css_selector('input[name="email"]').send_keys(fc_username)
driver.find_element_by_css_selector('input[name="pass"]').send_keys(fc_password)
driver.find_element_by_css_selector('button[name="login"]').click()

#wait for redirection
sleep(9)
# click again on followers button
try:
	btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.-nal3')))
	btn.click()
except:
	print("Unexpected Error")
	
# wait for the followers list
sleep(12)

#scroll until the end ! require big timeout and internet connection 
def scroll(timeout):
	scroll_pause_time = timeout
	last_height = driver.execute_script("return document.querySelector('div.isgrP').scrollHeight")
	i = 0
	while True:
		driver.execute_script("document.querySelector('div.isgrP').scrollTo(0, document.querySelector('div.isgrP').scrollHeight);")
		sleep(scroll_pause_time)
		new_height = driver.execute_script("return document.querySelector('div.isgrP').scrollHeight")
		print("-------Scrolling : {}----------".format(i))
		if new_height == last_height:
			break
		last_height = new_height
		i = i + 1

scroll(5) # set the timeout depends on your hardware and internet connection

#main job : find all followers.
followers = driver.find_elements_by_css_selector('a.FPmhX')

print('we have {} follower'.format(len(followers)))

with open('{}.csv'.format(username), 'w') as f:
	csv_file = csv.writer(f)
	csv_file.writerow(["follower number", "follower full name"])


for i, follower in enumerate(followers):
	with open('{}.csv'.format(username), 'a') as f:
		csv_file = csv.writer(f)
		csv_file.writerow(["follower {}".format(i), follower.text])
	print(follower.text)
