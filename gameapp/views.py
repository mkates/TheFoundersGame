from django.shortcuts import render_to_response
from gameapp.models import *
from django.template import RequestContext, Context, loader
from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import render
from django.utils import simplejson
import math
import sys
import os

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
			print 'Cookie Already Set'
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
		starttext = "Brush.io wants to develop the next generation of smart toothbrushes. Using a Bluetooth-connected toothbrush, consumers can track and record their toothbrush habits, helping them reach brighter, cleaner smiles, and potentially saving them money on dental fees and insurance.  We are seeking $1 million in venture funding to help us reach our goals."
	elif gameid == 2:
		imgsrc = 'fashiongirlheadshot.png'
	elif gameid == 3:
		imgsrc = 'larryheadshot.png'
	return render_to_response('game.html',{'gameid':gameid,'img':imgsrc,'school':school,'starttext':starttext},context_instance=RequestContext(request))

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
		#Grab gameID
		gameID = int(request.GET['gameid'])
		
		#Calculate Score
		analysis = analyze(gameID,qA,mV)
		totalscore = analysis[0]
		didWell = analysis[1]
		didPoor = analysis[2]
		#Get player from cookies
		player = 0
		try:
			try:
				g = request.session['playerid']
				player = Player.objects.filter(id=g)[0]
			except:
				try:
					request.session['school']
					player = Player(school=str(request.session['school']))
					#player.save()
				except:
					player = Player(school="Undefined")
					#player.save()
						
			#gamedata = Gamedata(player=player,gameID=gameID,gamescore=totalscore,question1=qA[0], question2=qA[1], question3=qA[2], question4=qA[3], question5=qA[4], question6=qA[5], question7=qA[6], question8=qA[7], question9=qA[8], question10=qA[9], meter1=mV[0], meter2=mV[1], meter3=mV[2],meter4=mV[3],meter5=mV[4], meter6=mV[5], meter7=mV[6], meter8=mV[7], meter9=mV[8], meter10=mV[9])
			#gamedata.save()
		except:
			print sys.exc_info()[0]
	return render_to_response('result.html',{"qA":qA,'mV':mV,'score':totalscore,'didWell':didWell,'didPoor':didPoor},context_instance=RequestContext(request))



# Generates a score from 0-9 for a given slider scale
# Takes as input the question rank (-5 being extremely detrimental
# and 5 being extremely encouraging)
# metervalue goes from 0 to 7
def analyze(gameID,qA,mV):
	# Open file
	gamestring = 'gameapp/game'+str(gameID)+'answers.txt'
	f = open(gamestring,'r')
	
	# Variables 
	didWell = []
	didPoor = []
	#Get answers from text file and store in answer list
	answers = {}
	questions = {}
	for line in f:
		line = line.split(';')
		if line[0] == 'V':
			at = ''
			if len(line) == 5:
				at = line[4]
			answers[line[1]] = [line[2],line[3],at]
		elif line[0] == 'Q' or line[0] == 'FQ':
			questions[line[1]] = line[3]
	
	#Score questions asked
	quesscore = 0
	for i in qA:
		if answers[str(i)][1] == 'VIM' or answers[str(i)][1] == 'IMP':
			quesscore += 10
	print 'score: '+str(quesscore)
		
	#Score how questions rated
	ratescore = 0
	for j in range(len(qA)):
		scoreadd = 0
		val = answers[str(qA[j])][0]
		mov = movement(mV[j],mV[j+1])
		if val == 'N' and mov < 0:
			scoreadd = 10
		elif val == 'P' and mov > 0:
			scoreadd = 10
		elif val == 'X' and (mov != 1 or mov != -1):
			scoreadd = 10
		
		helptext = {}
		helptext['question'] = questions[str(qA[j])]
		helptext['answer'] = answers[str(qA[j])][2]
		if scoreadd == 10:
			if len(helptext['answer']) > 5:
				didWell.append(helptext)
			ratescore += 10
		else:
			if len(helptext['answer']) > 5:
				didPoor.append(helptext)
			
	finalscore = math.ceil(.3*quesscore + .7*ratescore)
	return [finalscore,didWell,didPoor]

#Auxiliary Movement Function
def movement(prev_value,new_value):
	change = new_value - prev_value
	if change == 0 and prev_value == 7:
		return  2
	elif change > 0 and prev_value != 7:
		return 1
	elif change == 0 and prev_value == 0:
		return -2
	elif change < 0 and prev_value != 0:
		return -1
	else:
		return 0
		