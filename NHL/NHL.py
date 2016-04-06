from lxml import html
import requests
import time
import os

today=time.strftime("%Y-%m-%d")
page = requests.get('http://xrxs.net/nhl/?date=%s' % today)
tree = html.fromstring(page.content)
games = tree.xpath('/html/body/div/div[2]/text()')

gameList = []
tList = []

counter = 0
for i in games:
	counter+=1
	if(len(i) != 1):
		gameList.append(tList)
		tList = []
		i = i.strip()
		tList.append(i)
		counter-=1
	else:
		tGame = tree.xpath('/html/body/div/div[2]/a[%d]/text()' % counter)
		tStream = tree.xpath('/html/body/div/div[2]/a[%d]/@href' % counter)
		if(len(tGame) != 0 and len(tStream) != 0):
			if(tGame[0].find("FRENCH") == -1):
				tGame.append(tStream[0])
				tList.append(tGame)
gameList.append(tList)
gameList.pop(0)
try:
	    os.remove('playlist.m3u')
except OSError:
	    pass
myFile = open('playlist.m3u', 'w+')
myFile.write("#EXTM3U\n")
for i in gameList:
	for j in range(1, len(i)):
		myFile.write("#EXTINF:0 tvg-id=\"NHL\" tvg-name=\"Game\" group-title=\"%s\" tvg-logo=\"https://upload.wikimedia.org/wikipedia/en/thumb/3/3a/05_NHL_Shield.svg/527px-05_NHL_Shield.svg.png\",%s (http)\n" %(i[0], i[j][0]))
		myFile.write("%s\n\n" %i[j][1])
