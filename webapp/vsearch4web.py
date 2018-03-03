from flask import Flask, render_template, request, escape, session
from flask import copy_current_request_context
from vsearch import search4letters
from threading import Thread

from DBcm import UseDatabase, ConnectionError
from checker import check_logged_in
from time import sleep

app = Flask(__name__)

if __name__ == '__main__':
    app.config['dbconfig'] = { 'host': '127.0.0.1',
                               'user': 'vsearch',
                               'password': 'vsearchpasswd',
                               'database': 'vsearchlogDB', }
else:
    app.config['dbconfig'] = { 'host': 'kfurue.mysql.pythonanywhere-services.com',
                               'user': 'kfurue',
                               'password': 'vsearchpasswd',
                               'database': 'kfurue$vsearchlogDB', }


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        sleep(15)
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """insert into log
                    (phrase, letters, ip, browser_string, results)
                    values
                    (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (req.form['phrase'],
                                req.form['letters'],
                                req.remote_addr,
                                req.user_agent.browser,
                                res))

    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    title = 'Here are your results:'
    try:
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except Exception as err:
        print('****Logging failed with this error:', str(err))
    return render_template('results.html',
                            the_title = title,
                            the_phrase = phrase,
                            the_letters = letters,
                            the_results = results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                            the_tite='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results
                    from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
            titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
            return render_template('viewlog.html',
                                    the_title='View Log',
                                    the_row_titles=titles,
                                    the_data=contents)
    except ConnectionError as err:
        print('Is your databae switched on? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
@check_logged_in
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'

app.secret_key = 'YouWillNeverGuess'

if __name__ == '__main__':
    app.run(debug=True)