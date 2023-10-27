import sqlite3

from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sis')
def sis():
    return render_template('gerenciamento_quartos.html')

if __name__ == '__main__':
    app.run()
