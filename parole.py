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

def join_words():
    a = ' '.join([g.db.get(w) for w in g.db.keys()])
    return a

def create_dic(wordlist):
    d = dict([(w, wordlist.count(w)) for w in wordlist])
    return d
#crea un dizionario con la dimensione in percentuale dei relativi tag
# vedi http://blog.jeremymartin.name/2008/03/efficient-tag-cloud-algorithm.html
def size(element):
    min=maxmin_dict(dictionary, 'min')
    max=maxmin_dict(dictionary, 'max')
    max_percent=15
    min_percent=1
    multiplier=(max_percent-min_percent)/(max-min)
    # element_size=min_percent+((max-(max-(element-min)))*(max_percent-min_percent)/(max-min)

def tag_cloud(dictionary):
    tag_dict=dict([(dictionary[i], size(dictionary[i])) for i in dictionary])
    return tag_dict
#calcola per ogni elemento del dizionario la dimensione del tag nel cloud
def maxmin_dict(dictionary, mode):
    if (mode == 'max'):
        max = -1
        for k in dictionary.keys():
            if (dictionary[k] > max):
                max=dictionary[k]
        return max
    else:
        min = sys.max
        for k in dictionary.keys():
            if (dictionary[k] < min):
                min = dictionary[k]
        return min

@app.route('/cloud')
def show_cloud():
    dizionario = tag_cloud(create_dic(join_words()))
    return render_template('cloud.html', dict=dizionario)

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


