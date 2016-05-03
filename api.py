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
                     summonerNames=params["summonerNames"],     # multiple summoner names should be
                     api_key=API_KEY)                           # in a form of "name1,name2"
    response = urllib.urlopen(url)          # get response from API
    responseStr = response.read()           # read the response into string
    jsonDict = json.loads(responseStr)      # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def getMatchList(params):
    """
    Fetch summoner's match list
    :param params: {"region": "...", "summonerId": "..."}
    :return: {
                "matches": [
                    {
                        "lane": "MID",
                        "champion": 38,
                        "platformId": "EUW1",
                        "season": "SEASON2015",
                        "region": "EUW",
                        "matchId": 2120255420,
                        "queue": "RANKED_SOLO_5x5",
                        "role": "SOLO",
                        "timestamp": 1432334472308
                    }
                    ...
                ]
             }
    """
    url = 'https://{region}.api.pvp.net' \
          '/api/lol/{region}/v2.2/matchlist/by-summoner/{summonerId}' \
          '?api_key={api_key}'
    url = url.format(region=params["region"],
                     summonerId=params["summonerId"],   # multiple summoner names should be
                     api_key=API_KEY)   # in a form of "name1,name2"
    response = urllib.urlopen(url)      # get response from API
    responseStr = response.read()       # read the response into string
    jsonDict = json.loads(responseStr)  # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def filterMatchListByChampion(matchList, championId):
    """
    :param matchList: match list to be filtered
    :param championId: champion ID
    :return: filtered match list
    """
    filterMatchList = {"matches": []}
    for matchDict in matchList["matches"]:
        if matchDict["champion"] == championId:     # if champion ID equals
            filterMatchList["matches"].append(matchDict)
    return filterMatchList


def getMatchByMatchId(params):
    """
    :param params: {"region": "...", "matchId": "..."}
    :return: {
                  "queueType": "RANKED_SOLO_5x5",
                  "matchVersion": "5.9.0.318",
                  "platformId": "EUW1",
                  "season": "SEASON2015",
                  "region": "EUW",
                  "matchId": 2120255420,
                  "mapId": 11,
                  "matchCreation": 1432334472308,
                  "teams": [...],
                  "participants": [
                    {
                      "stats": {...},
                      "championId": 91,
                      "participantId": 1,
                      "runes": [...],
                      "highestAchievedSeasonTier": "PLATINUM",
                      "masteries": [
                        {
                          "masteryId": 4111,
                          "rank": 1
                        },
                        ...
                      ],
                      "spell2Id": 14,
                      "teamId": 100,
                      "timeline": {...},
                      "spell1Id": 4
                    },
                    ...
                  ],
                  "matchMode": "CLASSIC",
                  "matchDuration": 2171,
                  "participantIdentities": [
                    {
                        "player": {
                        "profileIcon": 19,
                        "summonerId": 27952221,
                        "matchHistoryUri": "/v1/stats/player_history/EUW1/31819470",
                        "summonerName": "Malm"
                      },
                      "participantId": 1
                    },
                    ...
                  ],
                  "matchType": "MATCHED_GAME"
             }
    """
    url = 'https://{region}.api.pvp.net' \
          '/api/lol/{region}/v2.2/match/{matchId}' \
          '?api_key={api_key}'
    url = url.format(region=params["region"],
                     matchId=params["matchId"],         # multiple summoner names should be
                     api_key=API_KEY)   # in a form of "name1,name2"
    response = urllib.urlopen(url)      # get response from API
    responseStr = response.read()       # read the response into string
    jsonDict = json.loads(responseStr)  # convert the string into JSON dictionary
    return filterJSONDict(jsonDict)


def printJSONDict(jsonDict):
    """
    Print a nested dictionary in a pretty way
    :param jsonDict: JSON dictionary
    """
    print json.dumps(jsonDict, sort_keys=False, indent=2)


def getMasteriesBySummonerAndChampion(summonerName, championId):
    """
    Find a summoner's latest mastery page of given champion
    :param summonerName: summoner's name
    :param championId: champion ID
    :return: the mastery page
    """
    summonerDict = getSummoners({"region": "euw", "summonerNames": summonerName})

    # Get summoner's ID
    if summonerDict:
        nameInLowerCase = list(summonerDict)[0]
        summonerId = summonerDict[nameInLowerCase]["id"]
    else:
        exit(1)

    # Get summoner's match list
    matchList = getMatchList({"region": "euw", "summonerId": summonerId})
    if matchList:
        # Get summoner's match ID list by specifying champion ID
        filteredMatchList = filterMatchListByChampion(matchList, championId)
        matchIdList = [match["matchId"] for match in filteredMatchList["matches"]]
        latestMatchID = matchIdList[0]  # get the lastest one
    else:
        exit(1)

    # Get match by match ID
    match = getMatchByMatchId({"region": "euw", "matchId": latestMatchID})
    if match:
        # Get masteries by champion ID
        for participant in match["participants"]:
            if participant["championId"] == championId:
                return participant["masteries"]
    else:
        exit(1)


def main():
    masteries = getMasteriesBySummonerAndChampion("FishKay", 38)
    printJSONDict(masteries)


if __name__ == "__main__":
    main()
