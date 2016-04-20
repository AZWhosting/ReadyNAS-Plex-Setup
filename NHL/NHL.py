from lxml import html
import requests
from requests.exceptions import ConnectionError
import time
import os
import sys
reload (sys)
sys.setdefaultencoding("utf-8")
import unicodedata
import datetime

def removeAccents(input_str):
	nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def todayTime():
	return time.strftime("%Y-%m-%d")

def getTree(today):
	try:
		page = requests.get('http://xrxs.net/nhl/?date=%s' % today)
	except ConnectionError:
		time.sleep(5)
		page = requests.get('http://xrxs.net/nhl/?data=%s' % today)

	return html.fromstring(page.content)

def getTodaysGames():
	today = todayTime()
	tree = getTree(today)
	gameTree = tree.xpath('/html/body/div/div[2]/text()')
	todayGameList = []
	gameQualityList = []
	counter = 0
	for game in gameTree:
		counter+=1
		if(len(game) != 1):
			todayGameList.append(gameQualityList)
			gameQualityList = []
			game = game.strip()
			game = removeAccents(game)
			gameQualityList.append(game)
			counter-=1
		else:
			tempGame = tree.xpath('/html/body/div/div[2]/a[%d]/text()' % counter)
			tempStream = tree.xpath('/html/body/div/div[2]/a[%d]/@href' % counter)
			if(len(tempGame) != 0 and len(tempStream) != 0):
				if(tempGame[0].find("FRENCH") == -1):
					tempGame.append(tempStream[0])
					gameQualityList.append(tempGame)
	todayGameList.append(gameQualityList)
	todayGameList.pop(0)
	return todayGameList

def writeToFile(todayGameList):
	try:
		os.remove('playlist.m3u')
	except OSError:
	    pass
	playlistFile = open('playlist.m3u', 'w+')
	playlistFile.write("#EXTM3U\n")
	for game in todayGameList:
		for quality in range(1, len(game)):
			playlistFile.write("#EXTINF:0 tvg-id=\"NHL\" tvg-name=\"Game\" group-title=\"%s\" tvg-logo=\"https://upload.wikimedia.org/wikipedia/en/thumb/3/3a/05_NHL_Shield.svg/527px-05_NHL_Shield.svg.png\",%s (http)\n" %(game[0], game[quality][0]))
			playlistFile.write("%s\n\n" %game[quality][1])
	playlistFile.close()

def main():
	todaysGameList = getTodaysGames()
	writeToFile(todaysGameList)

if __name__ == "__main__":
	    main()
