from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from models import Rule, Line, RuleSet, Modification, SelectedWitnesses
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from itertools import chain
from django.template import RequestContext

import pprint
import jsonpickle
import json
import httplib2
from urllib import urlencode
from urllib2 import Request, urlopen
import HTMLParser

regWitnesses = {}
regInfo = {}
baseTCWitnesses = {}
collationLine = -1
baseTokens = {}
baseWitnesses = {}

def getEntityApi(request):
    #url = "http://textualcommunities.usask.ca/drc/admin/det/det/"
    #url = "http://textualcommunities.usask.ca/drc/admin/det/element/21817/"
    #url = "http://textualcommunities.usask.ca/drc/api/text/14316/progress/"
    url = "http://textualcommunities.usask.ca/drc/api/text/12963/"

    send = httplib2.Http()
    response, content = send.request(url, 'GET')

    print content

    return HttpResponse("OK")

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









def regularization(request):
    # request should contain json with username and urn

    urn = "urn:det:TCUSASK:CTP2:entity=MI:Tale=MI:Line=IR"
    userName = "eks691@mail.usask.ca"

    #sendChooseTexts(username, urn)
    jdata = getWitnessData(urn)

    return render_to_response('jsRegularize/chooseTexts_interface.html', {"userName" : userName, "urn" : urn, "witnesses" : jdata}, context_instance=RequestContext(request))
    
def getWitnessData(urn):
    parser = HTMLParser.HTMLParser()
    jdata = '{"witnesses":['
    number = 0

    urlDoc = "http://textualcommunities.usask.ca/drc/api/urn/" + urn + "/"
    urlText = "http://textualcommunities.usask.ca/drc/api/text/"
    urlDet = "http://textualcommunities.usask.ca/drc/api/det/"

    ## comment out if urls start working again
    jdata = getTestData()
    return jdata

    send = httplib2.Http()
    response, content = send.request(urlDoc, 'GET')

    documentInfo = json.loads(content)
    
    for witness in documentInfo['hastextof']:
        url = urlText + str(witness) + "/"
        response, content = send.request(url, 'GET')
        text = json.loads(content)
        #print content

        url = urlDet + str(text['istextin']) + "/"
        # #print url
        try:
            response, content = send.request(url, 'GET')
            det = json.loads(content)

            if number != 0:
                jdata = jdata + ','
            jdata = jdata + '{"urn": ' + jsonpickle.encode(det['urn']) + ','
            #print det['urn']
            
            _id = det['urn'].split("document=")[1]
            _id = "".join(_id)
            _id = _id.split(":")[0]
            _id = "".join(_id)
            #jdata = jdata + '"id": ' + jsonpickle.encode(_id) + ','
            jdata = jdata + '"id": ' + jsonpickle.encode(_id) + '}'
            # print _id

            #jdata = jdata + '"img": ' + jsonpickle.encode(det['img']) + ','
            # print det['img']

            x = text['xml'].split("\n")
            x = "".join(x)
            x = x.split(">", 1)[1]
            x = "".join(x)
            x = x.split("</l>")[:-1]
            x = "".join(x)
            x = x.split("<hi rend=\"u\">")
            x = "".join(x)
            x = x.split("</hi>")
            x = "".join(x)
            x = x.split("<hi rend=\"bold\">")
            x = "".join(x)
            x = x.split("<hi rend=\"orncp\">")
            x = "".join(x)
            x = x.split("<lb n=\"\">")
            x = "".join(x)
            x = x.split("</lb>")
            x = "".join(x)
            x = x.split("<hi rend=\"unex\">")
            x = "".join(x)
            x = x.split("<hi rend=\"sup\">")
            x = "".join(x)
            x = x.split("<hi rend=\"ud\">")
            x = "".join(x)
            # x = x.split("&lt;gap extent=&quot;")
            # if(len(x) >= 2):
            #     x[1] = x[1][1:]
            # x = "".join(x)
            # x = x.split("&quot;&gt;&lt;/gap&gt;")
            # x = "".join(x)
            x = x.replace("&amp;", "&")
            x = parser.unescape(x)
            #jdata = jdata + '"content": ' + jsonpickle.encode(x) + '}'
            #print x

            number = number + 1
            #print text['istextin']
        except ValueError:
            print "valueError: " + str(text['istextin'])

    jdata = jdata + ']}'
    #pprint.pprint(jdata)

    return jdata

@csrf_exempt
def postSelectedWitnesses(request):
    if request.is_ajax():
       if request.method == 'POST':
           request.session['selectedWitnesses'] = request.raw_post_data
           #jdata = request.raw_post_data
           #print jdata

    return HttpResponse("OK")

def chooseRuleSetsInterface(request):
    if request.session.get('selectedWitnesses'):
        jdata = request.session.pop('selectedWitnesses')
        jdata = json.loads(jdata)
        userName = jdata['userName']
        urn = jdata['urn']
        witnesses = '{"witnesses":[' + jsonpickle.encode(jdata['witnesses']) + ']}'
        #print witnesses
        
        return render_to_response('jsRegularize/chooseRuleSets_interface.html', {"userName" : userName, "urn" : urn, "witnesses" : witnesses}, context_instance=RequestContext(request))

def postSelectedRuleSets(request):
    

    return HttpResponse("OK")

def getTestData():
    contentEl = 'Heere bigynneth the Miller; his tale'
    contentDb = 'Heere bygynneth the Millers tale ;'
    contentHg = 'Here bigynneth / the Millerys tale ~'
    contentAd2 = 'Incipit fabula Molendinarij'
    contentAd3 = 'Here endyth the prolog Here bygynneth the Millers tale'
    contentBo1 = 'Here begynnet; the Millers tale'
    contentCh = 'Here begynnet; the Milleris tale'
    contentCx1 = 'Here begynnet; the Milleres tale .'
    contentCx2 = 'Here begynneth the mylleres tale'
    contentDl = 'Here bee gynnit the tale'
    contentDs1 = 'And hiere beginneth the Millers tale.'
    contentEn1 = 'Here bygynnet; the Millers prologe'

    jdata = json.dumps({"witnesses": [{ "id": "El", "content" : contentEl }, { "id": "Db", "content" : contentDb }, { "id": "Hg", "content" : contentHg }, { "id": "Ad2", "content" : contentAd2 }, { "id": "Ad3", "content" : contentAd3 }, { "id": "Bo1", "content" : contentBo1 }, { "id": "Ch", "content" : contentCh }, { "id": "Cx1", "content" : contentCx1 }, { "id": "Cx2", "content" : contentCx2 }, { "id": "Dl", "content" : contentDl }, { "id": "Ds1", "content" : contentDs1 }, { "id": "En1", "content" : contentEn1 }]})

    return jdata
