from django.http import HttpResponseRedirect, HttpResponse
from models import Witness, Collation, Token, Rule
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

import pprint
import jsonpickle
import json
import httplib2

def loadInterface(request):
    return render_to_response('jsRegularize/interface.html')

def getBaseWitnesses(request):
    contentBo1 = '[4xcp]w[/4xcp]Whan that April with his shouris sote'
    contentBo2 = '[6orncp]W[/6orncp]hen that april; with his showres swote'
    contentCh = '[5emph]W[/5emph]han that Auerel wt his shoures soote'
    contentCx1 = '[3orncp]W[/3orncp]Han that Apprill with his shouris sote'
    contentCx2 = '[4orncp]W[/4orncp]Han that Apryll wyth hys shouris sote'
    contentEl = '[6orncp]W[/6orncp]Han that April with hise shoures soote'
    contentHa4 = '[6orncp]W[/6orncp]han that aprille with his schowres swoote'
    contentHg = '[6orncp]W[/6orncp]han that Aueryl wt his shoures soote'
    contentLa = '[xorncp]W[/xorncp]Han pat April wype his schoures soote .'
    contentTo1 = '[3emph]W[/3emph]hen that April . with his shouris . swote'

    jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : contentBo1 }, {"id" : "Bo2", "content" : contentBo2 }, {"id" : "Ch", "content" : contentCh }, {"id" : "Cx1", "content" : contentCx1 }, {"id" : "Cx2", "content" : contentCx2},{"id" : "El", "content" : contentEl }, {"id" : "Ha4", "content" : contentHa4 }, {"id" : "Hg", "content" : contentHg }, {"id" : "La", "content" : contentLa },\
{"id" : "To1", "content" : contentTo1 }]})

    return HttpResponse(jdata, mimetype="application/json")

def getBaseTokens(request):
    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    contentBo1 = '[4xcp]w[/4xcp]Whan that April with his shouris sote'
    contentBo2 = '[6orncp]W[/6orncp]hen that april; with his showres swote'
    contentCh = '[5emph]W[/5emph]han that Auerel wt his shoures soote'
    contentCx1 = '[3orncp]W[/3orncp]Han that Apprill with his shouris sote'
    contentCx2 = '[4orncp]W[/4orncp]Han that Apryll wyth hys shouris sote'
    contentEl = '[6orncp]W[/6orncp]Han that April with hise shoures soote'
    contentHa4 = '[6orncp]W[/6orncp]han that aprille with his schowres swoote'
    contentHg = '[6orncp]W[/6orncp]han that Aueryl wt his shoures soote'
    contentLa = '[xorncp]W[/xorncp]Han pat April wype his schoures soote .'
    contentTo1 = '[3emph]W[/3emph]hen that April . with his shouris . swote'

    jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : contentBo1 }, {"id" : "Bo2", "content" : contentBo2 }, {"id" : "Ch", "content" : contentCh }, {"id" : "Cx1", "content" : contentCx1 }, {"id" : "Cx2", "content" : contentCx2},{"id" : "El", "content" : contentEl }, {"id" : "Ha4", "content" : contentHa4 }, {"id" : "Hg", "content" : contentHg }, {"id" : "La", "content" : contentLa },\
{"id" : "To1", "content" : contentTo1 }]})

    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)

    #jdata2 = json.loads(content)
    #pprint.pprint(jdata2)
    
    return HttpResponse(content, mimetype="application/json")

@csrf_exempt
def saveRules(request):
    print "saveRules"
    if request.is_ajax():
       if request.method == 'POST':
           jdata = json.loads(request.raw_post_data)
           # print jdata

           for rule in jdata['rules']:
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
               r.json = ""
               r.save()

               # Rule.objects.all().delete();

    return HttpResponse("OK")

def getRules(request):
    
    jdata = '{"rules" : ['
    position = 0
    for r in Rule.objects.all():
        # print r.ruleID
        # print r.appliesTo
        # print r.condition
        # print r.action
        # print r.user
        # print r.scope
        # print r.regularization_type
        # print r.description
        # print r.token
        # print r.lemma
        # print r.json
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
        jdata = jdata + '"lemma":' + jsonpickle.encode(r.lemma) + ","
        jdata = jdata + '"json":' + jsonpickle.encode(r.json) + "}"
        position = position + 1
    jdata = jdata + ']}'

    # Rule.objects.all().delete()

    #jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : "soen" }, {"id" : "Bo2", "content" : "erin" }]})

    print jdata
        
    return HttpResponse(jdata, mimetype="application/json")
