from flask import Flask, render_template, request
from database import dbcon
from tagsearch import *

productlocator = locators.productLocator()
driverpath = 'D:\pythonasa\chromedriver.exe'

app = Flask(__name__)

searchkey = ''


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result')
def result():
    global searchkey
    try:
        searchkey = str(request.args.get('search'))
        page = int(request.args.get('pagen'))
    except ValueError as err:
        return render_template('404.html', message=err)

    if searchkey == None or searchkey =='':
        return render_template('404.html', message='empty search key huh. you should know better than that')
    if page < 0:
        return render_template('404.html', message='0th page...doesnt work')
    if page > 20:
        return render_template('404.html', message='no more than 20 page')
    res = begin(searchkey, int(page))
    if res == None:
        return render_template('404.html', message='no item to show')
    if res =='flag':
        return render_template('404.html',message='Connection timed out')
    return render_template('result.html', res=res)


@app.route('/del')
def deletion():
    return render_template('del.html')


@app.route('/deletion')
def findel():
    try:
        dele = str(request.args.get('del'))
        if dele is None or dele == '':
            return render_template('404.html', message='nothing to delete is nothing to delete')
        fin=dbcon.del_product(dele)
        return fin
    except:
        return render_template('404.html', message='error deleting the item')


@app.route('/showall')
def showall():
    res = dbcon.show_product()
    return render_template('result.html', res=res)


@app.route('/searchp')
def searchp():
    return render_template('searchp.html')


@app.route('/searched')
def searched():
    searched = request.args.get('searchp')
    resul = dbcon.show_single(searched)
    return render_template('result.html', res=resul)


if __name__ == '__main__':
    app.run(debug=True)
