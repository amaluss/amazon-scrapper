from flask import  Flask,render_template,request

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


app=Flask(__name__)

searchkey=''
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result')
def result():
    global searchkey
    searchkey=request.args.get('search')
    page = int(request.args.get('pagen'))
    res=begin(searchkey,page)
    if not searchkey:
        return render_template('404.html',message='empty search key huh. you should know better than that')
    if page<0:
        return render_template('404.html',message='0th page...doesnt work')
    if page>0:
        return render_template('404.html',message='no more than 20 pages')
    if res==None:
        return render_template('404.html', message='no item to show')
    print(searchkey,page,res)
    return render_template('result.html',res=res)

@app.route('/del')
def deletion():
    return render_template('del.html')

@app.route('/deletion')
def findel():

    try:
        dele = str(request.args.get('del'))
        if dele==None or dele=='':
            return render_template('404.html', message='nothng to delete is nothing to delete')
        dbcon.del_product(dele)
        return("succesfully deleted")
    except:
        return render_template('404.html',message='error deleting the item')

@app.route('/showall')
def showall():
    res=dbcon.show_product()
    return render_template('result.html', res=res)

@app.route('/searchp')
def searchp():
    return render_template('searchp.html')

@app.route('/searched')
def searched():
    searched=request.args.get('searchp')
    resul=dbcon.show_single(searched)
    print(resul)
    return render_template('result.html',res=resul)


def begin(searchkey,pages):
    for p in range(pages):
        url=f'https://www.amazon.in/s?k={searchkey}&page={p+1}&crid=2NHTI4S97L5Q0&qid=1656064805&sprefix=%2Caps%2C958&ref=sr_pg_{p+1}'
        chrome = webdriver.Chrome(executable_path=driverpath)
        chrome.get(url)
        div(chrome)
        chrome.close()
    return (dbcon.show_single(searchkey))

def div(chrome):
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


def convertint(s):
    cint=int(s.translate({ord(i): None for i in '₹ $,'}))
    return(cint)

if __name__=='__main__':
    app.run(debug=True)
