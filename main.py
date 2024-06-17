#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup
from datetime import timedelta
from datetime import datetime
from dateutil import tz


# TODO: Match the group values and show when game is done/what games have been played
# TODO: Make header

# NOTE: FOR DEBUGGING
# fixedTestTime = datetime.strptime("10:00:AM", "%H:%M:%p").strftime("%H:%M:%p")

class TimeNotRetrievedYetError(Exception):
    def __init__(self):
        self.msg = "Time not retrieved yet. Use Game().getData(self, key) before using this"
        super().__init__(self.msg)


class Game:
    def __init__(self, html_block):
        self.britishTime = None
        self.html_block = html_block
        self.TEAM = "swap-text__target"
        self.SCORE = "matches__teamscores-side"
        self.TIME = "matches__date"

    def getTeams(self):
        teams = self.html_block.find_all("span", "swap-text__target")
        team_list = [teams[0].text, teams[1].text]
        return team_list

    def getScore(self):
        score = self.html_block.find_all("span", "matches__teamscores-side")
        score_list = [score[0].text, score[1].text]
        for c, i in enumerate(score_list):
            score_list[c] = i.strip()
        return score_list

    def getMatchTime(self):
        time = self.html_block.find_all("span", "matches__date")[0].text
        return time.strip()

    def getData(self, key):
        value = self.html_block.find_all("span", key)
        returnFormat = []

        for item in value:
            returnFormat.append(item.text)

        for c, i in enumerate(returnFormat):
            returnFormat[c] = i.strip()

        if key == self.TIME:
            self.britishTime = returnFormat

        return returnFormat

    def convertTime(self):
        if self.britishTime is None:
            raise TimeNotRetrievedYetError

        # Can be improved
        utc = datetime.strptime(f"2022-11-25 {self.britishTime[0]}", "%Y-%m-%d %H:%M")
        utc = utc.replace(tzinfo=fromZone)
        return utc.astimezone(toZone).strftime('%H:%M:%p')

    def getWinningTeamIndex(self):
        intList = []
        score = self.getData(self.SCORE)
        for i in score:
            intList.append(i)
        if intList[0] == intList[1]: return None
        winIndex = score.index(max(intList))
        return winIndex

    def isGameCurrentlyOn(self):
        if self.britishTime is None:
            raise TimeNotRetrievedYetError

        gameStart = datetime.strptime(f"{self.convertTime()}", "%H:%M:%p")
        gameLength = timedelta(hours=2)
        gameEnds = (gameStart + gameLength).strftime("%H:%M:%p")
        currentTime = datetime.now().strftime("%H:%M:%p")

        gameStart = gameStart.strftime("%H:%M:%p")

        if gameStart <= currentTime <= gameEnds:
            return True
        elif currentTime >= gameEnds:
            return False
        else:
            return None


url = "https://www.skysports.com/euro-2024-fixtures"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
dayRegex = re.compile(r"(\w+ \d+)\w+ (\w+)")

fromZone = tz.gettz("Europe/London")
toZone = tz.tzlocal()


def getGamesInDay(day, writeTo, f):
    returnList = []
    game_list = []
    gameCountInDay = 0

    # Gets games played in that day
    for sibling in day.findNextSiblings():
        if str(sibling)[:3] == "<h4":
            # print(sibling.__str__()[:3] + ":" + str(gameCountInDay))
            break
        elif str(sibling)[:4] == "<div":
            # Every time there is a game
            # print(sibling.__str__()[:4])
            gameCountInDay += 1

    # Organizes the games in the day
    for row in range(gameCountInDay):
        if not game_list:
            game_list.append(day.findNextSibling())
        else:
            game_list.append(game_list[row - 1].findNextSibling())

    # Formats and finds the games in the day
    for c, game in enumerate(game_list):
        match = Game(game)

        teams = match.getData(match.TEAM)
        score = match.getData(match.SCORE)
        match.getData(match.TIME)

        timeLocal = match.convertTime()

        teamFormat = teams[0] + " vs " + teams[1]
        scoreFormat = f" [{score[0]} - {score[1]}]"
        timeFormat = f" Played at {timeLocal} (Local Time)"
        playing = match.isGameCurrentlyOn()

        if writeTo == "file":
            f.write(teamFormat + scoreFormat + timeFormat + "\n")
        elif writeTo == "console":
            print(teamFormat + scoreFormat + timeFormat + "\n")
        elif writeTo == "pygame":
            returnList.append([teams, score, timeLocal, 0, 90 * c, match.getWinningTeamIndex(), playing])
    return returnList


def writeToFile():
    with open("data.txt", "w") as f:
        s = soup.find_all("h4", "fixres__header2")
        print(len(s))
        for day in s:
            f.write(day.text + "\n")
            getGamesInDay(day, "file", f)
            f.write("\n")


def currentDay(displayType):
    dayNoSuffix = ""
    l = []
    matchFound = False
    s = soup.find_all("h4", "fixres__header2")
    for day in s:
        mo = dayRegex.match(day.text)
        if mo is not None:
            dayNoSuffix = mo.group(1) + " " + mo.group(2)
        if dayNoSuffix == dateToText():
            print(day.text)
            print("-" * 20 + "\n")
            l = getGamesInDay(day, displayType, None)
            l.append(dayNoSuffix)
            matchFound = True

    if not matchFound and displayType != "pygame":
        print("No more games today")

    if displayType == "pygame": return l


def dateToText():
    # Target format: dayofweek day month
    now = datetime.now()
    dayWeek = now.strftime('%A')
    day = now.strftime('%-d')
    month = now.strftime('%B')
    return f"{dayWeek} {day} {month}"