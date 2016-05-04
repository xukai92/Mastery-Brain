from flask import Flask, request, session, flash, redirect, url_for, render_template
import api


app = Flask(__name__)


@app.route('/')
def root():
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        summonerName = request.form['summonerName']
        championName = request.form['championName']
        region = request.form['region']
        print summonerName, championName, region
        # TODO: pass the formatted masteries to template
        return render_template('mastery.html', error=error)
    return render_template('search.html', error=error)


if __name__ == '__main__':
    app.run()
