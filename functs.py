# -*- coding: utf-8 -*-
import praw
import random
import json
from weather import Weather, Unit

client_id='c70sSiDnPW0LCA'
client_secret='ySyGNGudw-xrPuBoDIwlXmPDBp8'
user_agent='python:be.shibabot.topnewmemeapp:v1.0 (by /u/TheJeneverkoning)'

def initiatie(inputFile):
	with open(inputFile, 'r') as f:
		data = json.load(f)
	
	return data

def randomString(randomString):
	uitspraak = randomString[random.randint(0,len(randomString)-1)]
	print len(randomString)
	return uitspraak

def weerBericht(locatie):
    weather = Weather(unit= Unit.CELSIUS)
    location = weather.lookup_by_location(locatie)
    if (location != None):
        forecast = location.forecast[0]

        situatie = "Weerssituatie: " + forecast.text
        maxT = "Maximum temperatuur: " + forecast.high +u'\u2103'
        minT = "Minimum temperatuur: " +forecast.low +u'\u2103'

        return [situatie, maxT, minT]
    else:
        return "Geef een bestaande locatie in"



def getReddit(subred,lim,image):
    result = [0,""]
    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

    for submission in reddit.subreddit(subred).hot(limit=lim):
        if(image):
            if (submission.url[8]=="i"):
               result = mostRecent(submission,result)
     
        else:
            result = mostRecent(submission,result)
          
    
    return result[1]

def mostRecent(submission,result):
    
    if (submission.created>result[0]):
        return [submission.created,submission.url]
    else:
        return result
