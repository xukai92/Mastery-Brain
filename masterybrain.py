from flask import Flask, request, session, flash, redirect, url_for, render_template
import api


app = Flask(__name__)


@app.route('/')
def hello_world():
    masteries = api.getMasteriesBySummonerAndChampion("FishKay", 38)
    return str(masteries)


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('search'))
    print 3
    return render_template('search.html', error=error)


if __name__ == '__main__':
    app.run()
