from flask import Flask
import api

app = Flask(__name__)


@app.route('/')
def hello_world():
    masteries = api.getMasteriesBySummonerAndChampion("FishKay", 38)
    return str(masteries)


if __name__ == '__main__':
    app.run()
