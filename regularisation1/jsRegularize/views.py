from django.http import HttpResponseRedirect, HttpResponse
from models import Witness, Collation, Token
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
    contentWy = '[3orncp]W[/3orncp]han pt Apryll wuth his shoures sote'

    jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : contentBo1 }, {"id" : "Bo2", "content" : contentBo2 }, {"id" : "Ch", "content" : contentCh }, {"id" : "Cx1", "content" : contentCx1 }, {"id" : "Cx2", "content" : contentCx2},{"id" : "El", "content" : contentEl }, {"id" : "Ha4", "content" : contentHa4 }, {"id" : "Hg", "content" : contentHg }, {"id" : "La", "content" : contentLa },\
{"id" : "To1", "content" : contentTo1 }, {"id" : "Wy", "content" : contentWy}]})

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
    contentWy = '[3orncp]W[/3orncp]han pt Apryll wuth his shoures sote'

    jdata = json.dumps({"witnesses" : [{"id" : "Bo1", "content" : contentBo1 }, {"id" : "Bo2", "content" : contentBo2 }, {"id" : "Ch", "content" : contentCh }, {"id" : "Cx1", "content" : contentCx1 }, {"id" : "Cx2", "content" : contentCx2},{"id" : "El", "content" : contentEl }, {"id" : "Ha4", "content" : contentHa4 }, {"id" : "Hg", "content" : contentHg }, {"id" : "La", "content" : contentLa },\
{"id" : "To1", "content" : contentTo1 }, {"id" : "Wy", "content" : contentWy}]})

    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)
    pprint.pprint(content)
    
    return HttpResponse(content, mimetype="application/json")
