import redis
import string
from flask import Flask, request,  g, redirect, url_for, abort, \
render_template, flash
from datetime import date
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def create_redis_obj():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r

def word_count(s):
    c = len(string.split(s))
    return c

@app.before_request
def before_request():
    g.today = date.today()
    g.db=create_redis_obj()

@app.after_request
def after_request(response):
    del g.db
    return response

@app.route('/')
def show_entries():
    if g.db.exists(g.today):
        testo = g.db.get(g.today)
        if (len(testo)==0):
            testo=""
        if (word_count(testo) >= 750): 
             return render_template('layout.html', text=testo, sbloccato='true')
             flash('Hai inserito le tue 750 parole per oggi!')
        return render_template('layout.html', text=testo, sbloccato='false')
    return render_template('layout.html')

@app.route('/add', methods=['POST'])
def add_entry():
    g.db.set(g.today, request.form['text'])
    flash('Hai inserito ' + str(word_count(g.db.get(g.today))) + ' parole oggi')
    return redirect('/')

@app.route('/show')
def show():
    testo = g.db.get(g.today)
    return testo

if __name__ == '__main__':
        app.run(debug=True)


