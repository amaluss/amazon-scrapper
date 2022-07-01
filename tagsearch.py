import sqlite3
import time
import re

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import locators
import parser
from database import dbcon

productlocator=locators.productLocator()
driverpath='D:\pythonasa\chromedriver.exe'
'''def convertint(s):
    cint=int(s.translate({ord(i): None for i in '₹ $,'}))
    return(cint)


def div():
    expression = '[0-9]*%'
    WebDriverWait(chrome,10).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR,productlocator.users_broughttag)
        )
    )
    div = chrome.find_elements(by=By.CSS_SELECTOR, value=productlocator.divcard)
    for i in div:
        name = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.p_nametag)).text
        try:
            user_bcount = (i.find_element(by=By.CSS_SELECTOR, value='span.a-size-base.s-underline-text')).text
        except selenium.common.NoSuchElementException:
            user_bcount='0'
        price = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.price)).text
        try:
            og_price = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.ogpricetag)).text
            offer = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.offertag)).text
            percentlist = re.findall(expression, offer)
            if len(percentlist):
                percentage = percentlist[0]
            else:
                percentage = 'nil'
        except selenium.common.exceptions.NoSuchElementException:
            og_price = price
            percentage = 'nil'
        dbcon.product_insert(
            [name, convertint(user_bcount), convertint(price), convertint(og_price), percentage, searchkey])


def begin(searchkey,pages):
    for p in range(pages):
        url=f'https://www.amazon.in/s?k={searchkey}&page={p+1}&crid=2NHTI4S97L5Q0&qid=1656064805&sprefix=%2Caps%2C958&ref=sr_pg_{p+1}'
        chrome = webdriver.Chrome(executable_path=driverpath)
        chrome.get(url)
        div()
        chrome.close()
    return (dbcon.show_product())
'''


def begin(searchkey, pages):
    for p in range(pages):
        url = f'https://www.amazon.in/s?k={searchkey}&page={p + 1}&crid=2NHTI4S97L5Q0&qid=1656064805&sprefix=%2Caps%2C958&ref=sr_pg_{p + 1}'
        chrome = webdriver.Chrome(executable_path=driverpath)
        try:
            chrome.get(url)
        except selenium.common.exceptions.TimeoutException:
            chrome.close()
            return 'flag'
        div(chrome, searchkey)
        chrome.close()
    return dbcon.show_single(searchkey)


def div(chrome,searchkey):
    expression = '[0-9]*%'
    WebDriverWait(chrome, 10).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, productlocator.users_broughttag)
        )
    )
    div = chrome.find_elements(by=By.CSS_SELECTOR, value=productlocator.divcard)
    for i in div:
        name = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.p_nametag)).text
        try:
            user_bcount = (i.find_element(by=By.CSS_SELECTOR, value='span.a-size-base.s-underline-text')).text
        except selenium.common.NoSuchElementException:
            user_bcount = '0'
        price = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.price)).text
        try:
            og_price = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.ogpricetag)).text
            offer = (i.find_element(by=By.CSS_SELECTOR, value=productlocator.offertag)).text
            percentlist = re.findall(expression, offer)
            if len(percentlist):
                percentage = percentlist[0]
            else:
                percentage = 'nil'
        except selenium.common.exceptions.NoSuchElementException:
            og_price = price
            percentage = 'nil'

        dbcon.product_insert(
            [name, convertint(user_bcount), convertint(price), convertint(og_price), percentage, searchkey])


def convertint(s):
    cint = int(s.translate({ord(i): None for i in '₹ $,'}))
    return cint



