from django.http import HttpResponseRedirect, HttpResponse
from models import Witness, Collation, Token, Rule, Line
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from itertools import chain

import pprint
import jsonpickle
import json
import httplib2
import urllib
import HTMLParser

regWitnesses = {}
regInfo = {}
baseTCWitnesses = {}
collationLine = -1
baseTokens = {}
baseWitnesses = {}

def loadInterface(request):
    global collationLine
    collationLine = -1
    #return render_to_response('jsRegularize/interface.html')
    return render_to_response('jsRegularize/collate_interface.html')

def loadViewReg(request):
    return render_to_response('jsRegularize/view_reg.html')

def loadInformationWindow(request):
    return render_to_response('jsRegularize/information_window.html')

@csrf_exempt
def saveInformationWindow(request):
    if request.is_ajax():
       if request.method == 'POST':
           global regInfo
           regInfo = request.raw_post_data
           # print regInfo

    return HttpResponse("OK")

def getInformationWindow(request):
    print regInfo
    return HttpResponse(regInfo, mimetype="application/json")

@csrf_exempt
def saveRegWitnesses(request):
     if request.is_ajax():
       if request.method == 'POST':
           global regWitnesses
           regWitnesses = request.raw_post_data
           #print regWitnesses

     return HttpResponse("OK")

def getNextEntity(request):
    urlCollation = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'http://textualcommunities.usask.ca/drc/community/1/?entity='

    global collationLine
    collationLine = collationLine + 1
    entityNumber = collationLine * 2
    entityNumber = entityNumber + 12963

    if(entityNumber <= 14297):
        newUrl = url + str(entityNumber)
        send = httplib2.Http()
        response, content = send.request(newUrl, 'GET')
    
        jdata = refineWitnesses(content)

        send = httplib2.Http()
        response, content = send.request(urlCollation, 'POST', jdata, headers)

        global baseTokens
        baseTokens = content
    
        return HttpResponse(content, mimetype="application/json")

    if(entityNumber > 14297):
        return HttpResponse(baseTokens, mimetype="application/json")

def getPreviousEntity(request):
    urlCollation = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'http://textualcommunities.usask.ca/drc/community/1/?entity='

    global collationLine
    collationLine = collationLine - 1

    if(collationLine >= 0):
        entityNumber = collationLine * 2
        entityNumber = entityNumber + 12963

        newUrl = url + str(entityNumber)
        send = httplib2.Http()
        response, content = send.request(newUrl, 'GET')
    
        jdata = refineWitnesses(content)

        send = httplib2.Http()
        response, content = send.request(urlCollation, 'POST', jdata, headers)

        global baseTokens
        baseTokens = content
    
        return HttpResponse(content, mimetype="application/json")
    
    if(collationLine < 0):
        return HttpResponse(baseTokens, mimetype="application/json")

def refineWitnesses(content):
    parser = HTMLParser.HTMLParser()
    jdata = '{"witnesses":['
    position = 0
    witnessList = []
    
    content = content.split("<ul>")
    content = content[2:] 
    content = "".join(content)
    content = content.split("</ul>")
    content = content[:1]
    content = "".join(content)
    content = content.split("<li><p><b>")
    content = content[1:]

    for x in content:
        witnessId = x.split(":", 1)[0]
        found = False
        for wId in witnessList:
            if wId == witnessId:
                found = True
        if found == False:
            witnessList.append(witnessId)
            x = x.split(":", 1)[1]
            x = "".join(x)
            x = x.split("\n")
            x = "".join(x)
            x = x.split("&gt;", 1)[1]
            x = "".join(x)
            x = x.split("&lt;/l")[:-1]
            x = "".join(x)
            x = x.split("&lt;hi rend=&quot;u&quot;&gt;")
            x = "".join(x)
            x = x.split("&lt;hi rend=&quot;bold&quot;&gt;")
            if (x[0] == ""):
                x = x[1:]
            x = " ".join(x)
            x = x.split("&lt;/hi&gt;")
            x = "".join(x)
            x = x.split("&lt;lb n=&quot;&quot;&gt;")
            x = "".join(x)
            x = x.split("b&gt;")
            x = "".join(x)
            x = x.split("&lt;hi rend=&quot;orncp&quot;&gt;")
            x = "".join(x)
            x = x.split("&lt;hi rend=&quot;unex&quot;&gt;")
            x = "".join(x)
            x = x.split("&lt;hi rend=&quot;sup&quot;&gt;")
            x = "".join(x)
            x = x.split("&lt;hi rend=&quot;ud&quot;&gt;")
            x = "".join(x)
            x = x.split("&lt;gap extent=&quot;")
            if(len(x) >= 2):
                x[1] = x[1][1:]
            x = "".join(x)
            x = x.split("&quot;&gt;&lt;/gap&gt;")
            x = "".join(x)
            x = x.replace("&amp;", "&")
            x = parser.unescape(x)
            print witnessId + ": " + x

            if position != 0:
                jdata = jdata + ","
            jdata = jdata + '{"id":' + jsonpickle.encode(witnessId) + ","
            jdata = jdata +'"content":' + jsonpickle.encode(x) + "}"
            position = position + 1
    
    jdata = jdata + ']}'

    global baseWitnesses
    baseWitnesses = jdata

    return jdata

def getRegWitnesses(request):
    return HttpResponse(regWitnesses, mimetype="application/json")

def getBaseWitnesses(request):

    return HttpResponse(baseWitnesses, mimetype="application/json")

def getBaseTokens(request):
    
    return HttpResponse(baseTokens, mimetype="application/json")

@csrf_exempt
def saveRules(request):
    if request.is_ajax():
       if request.method == 'POST':
           jdata = json.loads(request.raw_post_data)
           # print jdata

           for rule in jdata['rules']:
               filteredRules = Rule.objects.filter(ruleID=rule['_id']).filter(\
                                            appliesTo=rule['appliesTo']).filter(\
                                            condition=rule['condition']).filter(\
                                            action=rule['action']).filter(\
                                            user=rule['user']).filter(\
                                            scope=rule['scope']).filter(\
                                            regularization_type=rule['regularization_type']).filter(\
                                            description=rule['description']).filter(\
                                            token=rule['token']).filter(\
                                            lemma=rule['lemma'])
               if not filteredRules:
                   r = Rule()
                   r.ruleID = rule['_id']
                   r.appliesTo = rule['appliesTo']
                   r.condition = rule['condition']
                   r.action = rule['action']
                   r.user = rule['user']
                   r.scope = rule['scope']
                   r.regularization_type=rule['regularization_type']
                   r.description = rule['description']
                   r.token=rule['token']
                   r.lemma=rule['lemma']
                   r.save()

               # Rule.objects.all().delete();

    return HttpResponse("OK")

@csrf_exempt
def changeRule(request):
    
    if request.is_ajax():
       if request.method == 'POST':
           jdata = json.loads(request.raw_post_data)
           print jdata

    ruleNum = 0
    for rule in jdata['rules']:
        if (ruleNum == 1):
            #add rule
            ruleNum = 0
            print "add rule"
            filteredRules = Rule.objects.filter(ruleID=rule['_id']).filter(\
                                            appliesTo=rule['appliesTo']).filter(\
                                            condition=rule['condition']).filter(\
                                            action=rule['action']).filter(\
                                            user=rule['user']).filter(\
                                            scope=rule['scope']).filter(\
                                            regularization_type=rule['regularization_type']).filter(\
                                            description=rule['description']).filter(\
                                            token=rule['token']).filter(\
                                            lemma=rule['lemma'])
            if not filteredRules:
                   r = Rule()
                   r.ruleID = rule['_id']
                   r.appliesTo = rule['appliesTo']
                   r.condition = rule['condition']
                   r.action = rule['action']
                   r.user = rule['user']
                   r.scope = rule['scope']
                   r.regularization_type=rule['regularization_type']
                   r.description = rule['description']
                   r.token=rule['token']
                   r.lemma=rule['lemma']
                   r.save()
                   
        elif(ruleNum == 0):
        	ruleNum = 1
       		print "delete rule"
        	Rule.objects.filter(ruleID=rule['_id']).filter(\
                                            appliesTo=rule['appliesTo']).filter(\
                                            condition=rule['condition']).filter(\
                                            action=rule['action']).filter(\
                                            user=rule['user']).filter(\
                                            scope=rule['scope']).filter(\
                                            regularization_type=rule['regularization_type']).filter(\
                                            description=rule['description']).filter(\
                                            token=rule['token']).filter(\
                                            lemma=rule['lemma']).delete()

    return HttpResponse("OK");

@csrf_exempt
def deleteRule(request):

    if request.is_ajax():
       if request.method == 'POST':
           jdata = json.loads(request.raw_post_data)
           print jdata

    for rule in jdata['rules']:
        filteredRules = Rule.objects.filter(ruleID=rule['_id']).filter(\
                                            appliesTo=rule['appliesTo']).filter(\
                                            condition=rule['condition']).filter(\
                                            action=rule['action']).filter(\
                                            user=rule['user']).filter(\
                                            scope=rule['scope']).filter(\
                                            regularization_type=rule['regularization_type']).filter(\
                                            description=rule['description']).filter(\
                                            token=rule['token']).filter(\
                                            lemma=rule['lemma']).delete()
        
    return HttpResponse("OK");

@csrf_exempt
def recollate(request):
    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    print "recollateNow"
    
    jdata = ""
    if request.is_ajax():
       if request.method == 'POST':
           jdata = request.raw_post_data

    pprint.pprint(json.loads(jdata))

    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)

    # jdata2 = json.loads(content)
    # pprint.pprint(jdata2)
    
    return HttpResponse(content, mimetype="application/json")

def getRules(request):
    
    jdata = '{"rules" : ['
    position = 0

    this_word = Rule.objects.filter(scope="this_word")
    this_block = Rule.objects.filter(scope="this_block")
    all_places = Rule.objects.filter(scope="all_places")

    rules = []
    if all_places and this_block and this_word :
        rules = list(chain(all_places, this_block, this_word))
    elif all_places and this_block:
        rules = list(chain(all_places, this_block))
    elif this_block and this_word:
        rules = list(chain(this_block, this_word))
    elif(all_places):
        rules = all_places
    elif(this_block):
        rules = this_block
    elif(this_word):
        rules = this_word
    else:
        rules = Rule.objects.all()
    
    for r in rules:
        if position != 0:
            jdata = jdata + ','
        jdata = jdata + '{"_id": ' + jsonpickle.encode(r.ruleID) + ","
        jdata = jdata + '"appliesTo":' + jsonpickle.encode(r.appliesTo) + ","
        jdata = jdata + '"condition":' + jsonpickle.encode(r.condition) + ","
        jdata = jdata + '"action":' + jsonpickle.encode(r.action) + ","
        jdata = jdata + '"user":' + jsonpickle.encode(r.user) + ","
        jdata = jdata + '"scope":' + jsonpickle.encode(r.scope) + ","
        jdata = jdata + '"regularization_type":' + jsonpickle.encode(r.regularization_type) + ","
        jdata = jdata + '"description":' + jsonpickle.encode(r.description) + ","
        jdata = jdata + '"token":' + jsonpickle.encode(r.token) + ","
        jdata = jdata + '"lemma":' + jsonpickle.encode(r.lemma) + "}"
        position = position + 1
    jdata = jdata + ']}'

    # Rule.objects.all().delete()

    #jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : "soen" }, {"id" : "Bo2", "content" : "erin" }]})

    pprint.pprint(jdata)
        
    return HttpResponse(jdata, mimetype="application/json")
