from django.shortcuts import render_to_response
from gameapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import render
from django.utils import simplejson
import math
import sys

def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))
	
def select(request):
	if request.method == 'GET':
		try:
			school = str(request.GET['school'])
			request.session['school'] = school
			try:
				request.GET['playerid']
			except:
				player = Player(school=school)
				player.save()
				request.session['playerid'] = player.id
		except:
			print 'Cookie Already Sey'
	return render_to_response('select.html',context_instance=RequestContext(request))

def play(request,gameid):
	return render_to_response('play.html',{'gameid':gameid},context_instance=RequestContext(request))

def talk(request,gameid):
	gameid = int(gameid)
	if gameid == 1:
		imgsrc = 'cartoonnerd.png'
	elif gameid == 2:
		imgsrc = 'fashiongirlfull.png'
	elif gameid == 3:
		imgsrc = 'larryfull.png'
	return render_to_response('talk.html',{'gameid':gameid,'img':imgsrc},context_instance=RequestContext(request))

def game(request,gameid):
	school = request.session['school']
	gameid = int(gameid)
	if gameid == 1:
		imgsrc = 'nerd.png'
	elif gameid == 2:
		imgsrc = 'fashiongirlheadshot.png'
	elif gameid == 3:
		imgsrc = 'larryheadshot.png'
	return render_to_response('game.html',{'gameid':gameid,'img':imgsrc,'school':school},context_instance=RequestContext(request))

def result(request):
	if request.method == 'GET':
		#Convert question response to a list
		qA = request.GET['questionsAsked']
		qA = qA.split(',')
		for i in range(len(qA)):
			qA[i] = int(qA[i])
			
		#Convert metricValues to a list
		mV = request.GET['meterValue']
		mV = mV.split(',')
		for i in range(len(mV)):
			mV[i] = int(mV[i])
		
		#Convert metricValues to a list
		pV = request.GET['pointvalues']
		pV = pV.split(',')
		for i in range(len(pV)):
			pV[i] = int(pV[i])
			
		#Calculate Score
		totalscore = 0;
		mVnew = [4] + mV
		for i in range(10):
			totalscore += score(pV[i],mVnew[i],mVnew[i+1])
		for val in qA:
			totalscore += pV[val]
		
		#Grab gameID
		gameID = int(request.GET['gameid'])
		player = 0
		try:
			try:
				g = request.session['playerid']
				print int(g)
				player = Player.objects.filter(id=g)[0]
				print player
			except:
				try:
					request.session['school']
					player = Player(school=str(request.session['school']))
					player.save()
				except:
					player = Player(school="Undefined")
					player.save()
			gamedata = Gamedata(player=player,gameID=gameID,gamescore=totalscore,question1=qA[0], question2=qA[1], question3=qA[2], question4=qA[3], question5=qA[4], question6=qA[5], question7=qA[6], question8=qA[7], question9=qA[8], question10=qA[9], meter1=mV[0], meter2=mV[1], meter3=mV[2],meter4=mV[3],meter5=mV[4], meter6=mV[5], meter7=mV[6], meter8=mV[7], meter9=mV[8], meter10=mV[9])
			gamedata.save()
		except:
			print sys.exc_info()[0]
	return render_to_response('result.html',{"qA":qA,'mV':mV,'score':totalscore},context_instance=RequestContext(request))



# Generates a score from 0-9 for a given slider scale
# Takes as input the question rank (-5 being extremely detrimental
# and 5 being extremely encouraging)
# metervalue goes from 0 to 7
def score(questioneffect,meterbefore,currentmeter):
	# If question has no impact
	if questioneffect == 0:	
		if meterbefore == currentmeter:
			return 8
		else :
			return 4
	#If question is slightly bad (-1 to -3)
	if questioneffect > -4 and questioneffect < 0:
		if meterbefore-currentmeter < 0 or currentmeter == 0:
			return 8
		elif meterbefore == currentmeter:
			return 5
		else:
			return 2
	
	#If question is slightly good (1 to 3)
	if questioneffect < 4 and questioneffect > 0:
		if meterbefore-currentmeter > 0 or currentmeter == 7:
			return 8
		elif meterbefore == currentmeter:
			return 5
		else:
			return 2
	
	#Really Bad Question (-4 to -5)
	if questioneffect < -3 or currentmeter == 0:
		if (meterbefore-currentmeter < 0):
			return 8
		else:
			return 1
			
	#Really Good Question (4 to 5)
	if questioneffect > 3 or currentmeter == 7:
		if meterbefore-currentmeter > 0:
			return 8
		else:
			return 1
	#Catch all
	return 5
