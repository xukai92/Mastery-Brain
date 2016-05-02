import json
import urllib

import confidential

API_KEY = confidential.API_KEY


def filterJSONDict(jsonDict):
    """
    Filter a JSON dictionary by checking if there is no response
    :param jsonDict: a dictionary from JSON response
    :return: returns None if reponse is not found, else the original dict
    """
    if jsonDict.has_key('status'):  # If the dictionary has a top level key
        return None                 # called "status", it means it doesn't
    else:                           # get the information needed
        return jsonDict


def getSummoners(params):
    """
    Fetch summoners' information
    :param params: {"region": "...", "summonerNames": "..."}
    :return: {
                u'{nameInLowercase}': {
                    u'profileIconId'    :   ...,
                    u'summonerLevel'    :   ...,
                    u'revisionDate'     :   ...,
                    u'id'               :   ...,
                    u'name'             :   ...
                }
             }
    """
    url = 'https://{region}.api.pvp.net' \
          '/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}' \
          '?api_key={api_key}'
    url = url.format(region=params["region"],
                     summonerNames=params["summonerNames"],  # multiple summoner names should be
                     api_key=API_KEY)                        # in a form of "name1,name2"
    response = urllib.urlopen(url)          # get response from API
    responseStr = response.read()           # read the response into string
    jsonDict = json.loads(responseStr)      # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


# TODO: finish getRecentMatches
def getRecentMatches(params):
    """
    Fetch summoner's recent mathces
    :param params:
    :return:
    """
    pass


# TODO: finish getMasteries
def getMasteries(params):
    """
    Fetch masteries from a summoner
    :param params:
    :return:
    """
    pass


# TODO: finish findMasteryByChampion
def findMasteryByChampion():
    """
    Given recent matches and a summoner's mastery pages,
    find
    :return:
    """
    pass


def printJSONDict(jsonDict):
    """
    Print a nested dictionary in a pretty way
    :param jsonDict: JSON dictionary
    """
    print json.dumps(jsonDict, sort_keys=False, indent=2)


def main():
    summonerDict = getSummoners({"region": "euw", "summonerNames": "FishKay"})
    if summonerDict:
        printJSONDict(summonerDict)
        nameInLowerCase = list(summonerDict)[0]
        summonerId = summonerDict[nameInLowerCase]["id"]
        summonerName = summonerDict[nameInLowerCase]["name"]
        print summonerId, summonerName
    else:
        exit(1)


if __name__ == "__main__":
    main()
