#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


class Game:
    def __init__(self, html_block):
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

        return returnFormat


url = "https://www.skysports.com/world-cup-fixtures"
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
dayRegex = re.compile(r"(\w+ \d+)\w+ (\w+)")


def getMatchesInDay(day, writeTo, f):
    game_list = []
    gameCountInDay = 0

    # Gets games played in that day
    for sibling in day.findNextSiblings():
        if sibling.__str__()[:3] == "<h4":
            # print(sibling.__str__()[:3] + ":" + str(gameCountInDay))
            break
        elif sibling.__str__()[:4] == "<div":
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
    for game in game_list:
        match = Game(game)

        teams = match.getData(match.TEAM)
        score = match.getData(match.SCORE)
        time = match.getData(match.TIME)

        teamFormat = teams[0] + " vs " + teams[1]
        scoreFormat = f" [{score[0]} - {score[1]}]"
        timeFormat = f" Played at {time[0]} (Qatar Time)"
        if writeTo == "file":
            f.write(teamFormat + scoreFormat + timeFormat + "\n")
        elif writeTo == "console":
            print(teamFormat + scoreFormat + timeFormat + "\n")


def writeToFile():
    with open("data.txt", "w") as f:
        s = soup.find_all("h4", "fixres__header2")
        print(len(s))
        for day in s:
            getMatchesInDay(day, "file", f)
            f.write("\n")


def currentGame():
    dayNoSuffix = ""
    matchFound = False
    s = soup.find_all("h4", "fixres__header2")
    for day in s:
        mo = dayRegex.match(day.text)
        if mo is not None:
            dayNoSuffix = mo.group(1) + " " + mo.group(2)
        if dayNoSuffix == dateToText():
            print(day.text)
            print("-"*20 + "\n")
            getMatchesInDay(day, "console", None)
            matchFound = True

    if not matchFound:
        print("No more games today")


def dateToText():
    # Target format: dayofweek day month
    now = datetime.now()
    dayWeek = now.strftime('%A')
    day = now.strftime('%-d')
    month = now.strftime('%B')
    return f"{dayWeek} {day} {month}"


currentGame()
