import MySQLdb
import string

from flask import Flask, g, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'PS#yio`%_!((f_or(%)))s'
# app.config.from_object('config')

from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)

@app.before_request
def before_request():
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT))

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'): g.db.close()



@app.route('/')
@app.route('/index')
def index():
    # if not session.get('logged_in'):
    #     return redirect(url_for('login'))
    # return redirect(url_for('edit'))
    return render_template('index.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        c = g.db.cursor()
        titleName = request.form['titleName']
        contentDetail = request.form['contentDetail']
        if len(contentDetail) < 140:
            contentSimple = contentDetail
        else:
            contentSimple = contentDetail[0:130]
        c.execute("insert into blog (titleName, contentSimple, contentDetail) values(%s, %s, %s)", (titleName, contentSimple, contentDetail ))
        return redirect(url_for('index'))
    return render_template('edit.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        c = g.db.cursor()
        c.execute("insert into students (stuId, password, email) values(%s, %s, %s)", (request.form['stuId'], request.form['password'], request.form['email'] ))
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        c = g.db.cursor()
        stuId = request.form['stuId']
        password = str(request.form['password'])
        c.execute("select password from students where stuId = '%s'" % stuId)
        msgs = c.fetchall()
        if not msgs :
            return redirect(url_for('login'))
        if not msgs[0][0] == password:
            return redirect(url_for('login'))
        # session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('login.html')
