# -*- coding: utf-8 -*-
from functs import randomString, initiatie, weerBericht, getReddit
import random

#verschillende functie classen

#geeft url van een meme uit reddit terug
class TopMeme:
	def __init__(self, description):
		self.data = []
		self.description = description

	def run(self):
		return [True, getReddit('dankmemes',10,True)]

#geeft url van recentste nieuwsartikel uit reddit
class TopNews:
	def __init__(self, description):
		self.data = []
		self.description = description

	def run(self):
		return getReddit('news',10,False)

#geeft een willekeurig blaf reactie terug
class Bark:
	def __init__(self, description):
		self.data = []
		self.description = description
		
	def run(self):
		if (random.randint(0,30) == 1):
			return bark[6]
		else:
			return bark[random.randint(0,5)]

#geeft een uistpraak van joran terug			
class JoranSpeak:
	def __init__(self, description):
		self.data = []
		self.description = description
	
	
	def run(self):
		if( joranInitiate == False ):
			joranSpeakList=initiatie('joran zijn uitspraken.json')
			joranInitiate == True
		return randomString(joranSpeakList["uitspraken"])

#geeft alle actieve commands weer met uitleg 
class Help:
	def __init__(self, description):
		self.data = []
		self.description = description
		
	def run(self):
		hulpString = []
		for key in sorted(functionList):
			hulpString.append(key +" - " + functionList[key].description)
			
		return hulpString

#geeft url van gif van rollende shiba terug		
class Roll:
	def __init__(self, description):
		self.data = []
		self.description = description
		
	def run(self):
		if (gifsInitiate==False):
			gifList=initiatie('gifs.json')
			gifsInitiate==True


		return [True,randomString(gifList["roll"])]

#geeft url van gif van pootjegevende shiba terug
class Paw:
	def __init__(self, description):
		self.data = []
		self.description = description
		
	def run(self):
		if (gifsInitiate==False):
			
			gifList=initiatie('gifs.json')
			gifsInitiate==True


		return [True,randomString(gifList["paw"])]

#geeft url van gif van dood spelende shiba terug
class Play_dead:
	def __init__(self, description):
		self.data = []
		self.description = description
		
	def run(self):
		if (gifsInitiate==False):

			gifList=initiatie('gifs.json')
			gifsInitiate==True


		return [True,randomString(gifList["play_dead"])]

#geeft geluidsfragment van blaffende shiba terug
class Wooof:
	def __init__(self, description):
		self.data=[]
		self.description = description

	def run(self):
		return [False,"http://shibabot.epizy.com/Woof.wav"]

#geeft willekeurige foto van shiba terug
class Shiba:
	def __init__(self, description):
		self.data=[]
		self.description = description

	def run(self):
		if (shibaPicsInitiate==False):
			shibaPicsList=initiatie('shiba pics.json')
			shibaPicsInitiate==True


		return [True,randomString(shibaPicsList["pics"])]

#geeft het weerbericht van opgegeven locatie terug
class Weerbericht:
	"""docstring for Weerbericht"""
	def __init__(self, description):
		self.data=[]
		self.description = description

	def run(self,location):
		return weerBericht(location)
		
bark = ["bark", "bork", "bark bark", "wooof", "waf waf", "gggrrrr", "Enslave all humans!"]
joranSpeakList = ""
gifList = ""
shibaPicsList = ""
shibaPicsInitiate= False
joranInitiate = False
gifsInitiate = False
functionList = { "joran": JoranSpeak("Wat zou joran hiervan zeggen?"),
				 "help": Help("Geeft lijst van bruikbare commando's."),
				 "bark": Bark("Laat shibabot blaffen."),
				 "roll": Roll("Shibabot voert een shibarol uit."),
				 "shiba": Shiba("Geeft foto van jouw shiba terug."),
				 "woof": Wooof("Laat je shiba blaffen."),
				 "play dead": Play_dead("Laat je Shiba dood spelen."),
				 "paw": Paw("Geef een pootje aan jouw Shiba"),
				 "weather": Weerbericht("Typ weather <locatie> om het weerbericht te zien."),
				 "news": TopNews("Geeft belangrijk recent nieuws terug"),
				 "meme": TopMeme("Haalt een trending meme boven")
				 }

	
def procesText(default ,message_text, variable):
	if message_text in functionList and message_text != "weather":
		if(variable != None):	
			return  functionList[message_text].run(variable)
		else:
			return functionList[message_text].run()
	else:
		return default