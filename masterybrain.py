from flask import Flask, request, redirect, url_for, render_template
import api


app = Flask(__name__)


@app.route('/')
def root():
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        # get query from form
        summonerName = request.form['summonerName']
        championName = request.form['championName']
        region = request.form['region']

        # get master info
        masteries = api.getMasteriesBySummonerAndChampion(summonerName, championName, region)
        if masteries:
            masterySet = api.formatMasteries(masteries)

            # format parameters
            param = dict()
            param["summonerName"] = summonerName
            param["championName"] = championName
            param["region"] = region
            param["masterySet"] = masterySet
            return render_template('mastery.html', error=error, param=param)
        else:
            error = "summoner name not found."
    return render_template('search.html', error=error)


if __name__ == '__main__':
    app.run()
