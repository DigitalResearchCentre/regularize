from django.http import HttpResponseRedirect, HttpResponse
from models import Witness, Collation, Token, Rule
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from itertools import chain

import pprint
import jsonpickle
import json
import httplib2
import urllib

regWitnesses = {}
regInfo = {}
baseTCWitnesses = {}

def loadInterface(request):
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

def getRegWitnesses(request):
    return HttpResponse(regWitnesses, mimetype="application/json")

def getBaseWitnesses(request):
    # getTCWitnesses()

    # jdata = json.dumps({"witnesses" : [{"id" : "Hg", "content" : baseTCWitnesses[0][0]}, {"id": "El", "content": baseTCWitnesses[1][0]}, {"id" : "Db", "content": baseTCWitnesses[2][0]},{"id": "Cp", "content": baseTCWitnesses[3][0]}]})

    contentBo1 = '[4xcp]w[/4xcp]Whan that Ap ri l with his shouris sote'
    contentBo2 = '[6orncp]W[/6orncp]hen that april; with his showres swote'
    contentCh = '[5emph]W[/5emph]han that Auerel wt his shoures soote'
    contentCx1 = '[3orncp]W[/3orncp]Han that Apprill with his shouris sote'
    contentCx2 = '[4orncp]W[/4orncp]Han that Apryll wyth hys shouris sote'
    contentEl = '[6orncp]W[/6orncp]Han that April with hise shoures soote'
    contentHa4 = '[6orncp]W[/6orncp]han that aprille with his schowres swoote'
    contentHg = '[6orncp]W[/6orncp]han that Aueryl wt his shoures soote'
    contentLa = '[xorncp]W[/xorncp]Han pat Ap ri l wype his schoures soote .'
    contentTo1 = '[3emph]W[/3emph]hen that Ap ri l . with his shouris . swote'

    jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : contentBo1 }, {"id" : "Bo2", "content" : contentBo2 }, {"id" : "Ch", "content" : contentCh }, {"id" : "Cx1", "content" : contentCx1 }, {"id" : "Cx2", "content" : contentCx2},{"id" : "El", "content" : contentEl }, {"id" : "Ha4", "content" : contentHa4 }, {"id" : "Hg", "content" : contentHg }, {"id" : "La", "content" : contentLa },\
{"id" : "To1", "content" : contentTo1 }]})

    return HttpResponse(jdata, mimetype="application/json")

def getBaseTokens(request):
    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    contentBo1 = '[4xcp]w[/4xcp]Whan that Ap ri l with his shouris sote'
    contentBo2 = '[6orncp]W[/6orncp]hen that april; with his showres swote'
    contentCh = '[5emph]W[/5emph]han that Auerel wt his shoures soote'
    contentCx1 = '[3orncp]W[/3orncp]Han that Apprill with his shouris sote' 
    contentCx2 = '[4orncp]W[/4orncp]Han that Apryll wyth hys shouris sote'
    contentEl = '[6orncp]W[/6orncp]Han that April with hise shoures soote'
    contentHa4 = '[6orncp]W[/6orncp]han that aprille with his schowres swoote'
    contentHg = '[6orncp]W[/6orncp]han that Aueryl wt his shoures soote'
    contentLa = '[xorncp]W[/xorncp]Han pat Ap ri l wype his schoures soote .'
    contentTo1 = '[3emph]W[/3emph]hen that Ap ri l . with his shouris . swote'

    jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : contentBo1 }, {"id" : "Bo2", "content" : contentBo2 }, {"id" : "Ch", "content" : contentCh }, {"id" : "Cx1", "content" : contentCx1 }, {"id" : "Cx2", "content" : contentCx2},{"id" : "El", "content" : contentEl }, {"id" : "Ha4", "content" : contentHa4 }, {"id" : "Hg", "content" : contentHg }, {"id" : "La", "content" : contentLa },\
{"id" : "To1", "content" : contentTo1 }]})

    # jdata = json.dumps({"witnesses" : [{"id" : "Hg", "content" : baseTCWitnesses[0][0]}, {"id": "El", "content": baseTCWitnesses[1][0]}, {"id" : "Db", "content": baseTCWitnesses[2][0]},{"id": "Cp", "content": baseTCWitnesses[3][0]}]})
    
    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)
    
    return HttpResponse(content, mimetype="application/json")

def getTCWitnesses():
    urlHg = 'http://textualcommunities.usask.ca/drc/community/1/?doc=14316&text=16374#tabs-2'
    urlEl = 'http://textualcommunities.usask.ca/drc/community/1/?doc=16373&text=16374#tabs-2'
    urlDb = 'http://textualcommunities.usask.ca/drc/community/1/?doc=15690&text=16374#tabs-2'
    urlCp = 'http://textualcommunities.usask.ca/drc/community/1/?doc=15003&text=16374#tabs-2'
    
    send = httplib2.Http()
    response, content = send.request(urlHg, 'GET')
    contentHg = getWitnessesHTML(content)
    # print contentHg

    response, content = send.request(urlEl, 'GET')
    contentEl = getWitnessesHTML(content)
    # print contentEl

    response, content = send.request(urlDb, 'GET')
    contentDb = getWitnessesHTML(content)
    # print contentDb

    response, content = send.request(urlCp, 'GET')
    contentCp = getWitnessesHTML(content)
    # print contentCp

    global baseTCWitnesses
    baseTCWitnesses = [contentHg, contentEl, contentDb, contentCp]
    
    # return HttpResponse("OK")

def getWitnessesHTML(content):
    content = content.split("<span><lb />")
    content = content[1:] 
    content = "".join(content)
    content = content.split("\n")
    content = "".join(content)
    content = content.split("<div>")
    content = "".join(content)
    content = content.split("</div>")
    content = "".join(content)
    for i in range(0, 50):
        content = content.split("<span>"+str(i)+"</span>")
        content = "".join(content)
        content = content.split("<l n="+str(i)+">")
        content = "".join(content)
    content = content.split("<span>")
    content = "".join(content)
    content = content.split("<div class")
    content = content[:-3]
    content = "".join(content)
    content = content.split("  ")
    content = "".join(content)
    content = content.split("<hi rend=orncp>")
    content = "".join(content)
    content = content.split("<hi rend=sup>")
    content = "".join(content)
    content = content.split("<l n=IR>")
    content = "".join(content)
    content = content.split("</hi>")
    content = "".join(content)
    content = content.split("<hi rend=bold>")
    content = "".join(content)
    content = content.split("</l></span>")
    content = content[:-1]
    #content = "".join(content)
    
    return content

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
