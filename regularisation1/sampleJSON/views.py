from django.http import HttpResponseRedirect, HttpResponse
from models import Witness, Collation, Token
from django.views.decorators.csrf import csrf_exempt
from forms import RegularizationForm
from django.shortcuts import render_to_response

import pprint
import jsonpickle
import json
import httplib2

def collate(request):

    # get data from form, send to collatex engine and send resultant collation
    # onto the page that can change the collation
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
    # print response
    # print content
 
    jdata = json.loads(content)
    # pprint.pprint(jdata)

    # saving collation to database
    # c = Collation()
    # c.save()
    for data in jdata['alignment']:
        # print data['witness']
        # print data['tokens'][2]['t']
        content = ""
        pos = 0
        filteredWitness = None
        filteredWitness = Witness.objects.filter(witnessId=data['witness'])
        if not filteredWitness:
            w = Witness()
            w.witnessId = data['witness']
            w.save() #must save before can add to manytomanyfield of witness
        for token in data['tokens']:
            if token != None:
                filteredToken = None
                filteredToken = Token.objects.filter(\
                                                content=token['t']).filter(\
                                                normalized=token['n']).filter(\
                                                position=pos).filter(\
                                                witnessId=data['witness'])
                if not filteredToken:
                    # print token['t']
                    content = content + token['t'] + " "
                    t = Token.objects.create(content=token['t'],\
                                             normalized=token['n'],\
                                             position=pos,\
                                             witnessId=data['witness'])
                    if not filteredWitness:
                        w.tokenList.add(t)
                        w.save()
            else:
                filteredToken = None
                filteredToken = Token.objects.filter(\
                                                content="").filter(\
                                                normalized="").filter(\
                                                position=pos).filter(\
                                                witnessId=data['witness'])
                if not filteredToken:
                    t = Token.objects.create(content="",\
                                             normalized="",\
                                             position=pos,\
                                             witnessId=data['witness'])
                    if not filteredWitness:
                        w.tokenList.add(t)
                        w.save()
            pos = pos + 1
        if not filteredWitness:
            # print content
            w.content = content
            # print w
            w.save() # changes to databases only happen with .save() is called
                     #c.witnessList.add(w)
                     #c.save()

    return HttpResponseRedirect('/regularization/sample/regularize/000/')

@csrf_exempt
def regularize(request, pos):
    
    form = RegularizationForm(request.POST or None)

    # if the done button was pressed
    if request.method == 'POST':
        submit = request.POST.get('done', None)
        if submit:
            # delete all objects in the databases
            Token.objects.all().delete()
            Witness.objects.all().delete()
            Collation.objects.all().delete()
            
        submit = request.POST.get('next', None)
        if submit:
            # goto the next token/variant for regularization
            # TODO:: warning when at end of token list
            position = int(pos) + 1
            if position < 10:
                position = '00' + str(position)
            elif position < 100:
                position = '0' + str(position)
            else:
                position = str(position)
            url = '/regularization/sample/regularize/' + position + '/'
            print url
            return HttpResponseRedirect(url)

        submit = request.POST.get('back', None)
        if submit:
            # goto the last token/variant for regularization
            # TODO: 
            if int(pos) != 0:
                position = int(pos) - 1
                if position < 10:
                    position = '00' + str(position)
                elif position < 100:
                    position = '0' + str(position)
                else:
                    position = str(position)
                url = '/regularization/sample/regularize/' + position + '/'
                return HttpResponseRedirect(url)

        submit = request.POST.get('ok', None)
        if submit:
            # regularize
            # TODO: do different things for different reg_choices
            if request.method == 'POST' and form.is_valid():
                reg_this = form.cleaned_data['reg_this']
                reg_to = form.cleaned_data['reg_to']
                choice = form.cleaned_data['reg_choices']
                # print choice
                if reg_this != "":
                    if reg_this == 'None':
                        reg_this = ''
                    # change database to reflect regularize
                    # TODO: update positions if two words or get rid of word,etc
                    tokens = Token.objects.filter(position=pos)
                    for t in tokens:
                        if t.content == reg_this:
                            t.original = reg_this
                            t.content = reg_to
                            t.save()
                    # TODO: make a rule -> JSON
                else:
                    # TODO: send user a error message
                    print "error"

        submit = request.POST.get('recollate', None)
        if submit:
            #recollate
            if request.method == 'POST' and form.is_valid():
                recollate()

        submit = request.POST.get('view', None)
        if submit:
            # view changes
            if request.method == 'POST' and form.is_valid():
                return HttpResponseRedirect('/regularization/show/')

    # find the distinct tokens for particular position
    tokens = Token.objects.filter(position=pos).distinct('content')
    allTokens = Token.objects.filter(position=pos)
    # print tokens

    # build the token content for the regularization area
    content = ""
    for t in tokens:
        if t.content == "":
            content = content + "None" + " "
        else:
            content = content + t.content + " "
        for a in allTokens:
            if a.content == t.content:
                content = content + a.witnessId + " "
        content = content + " / "

    data = {'reg_area': content}
    form = RegularizationForm(data)

    return render_to_response('input/change.html', {'form': form})

def getWitnesses(request):

    jdata = '{"witnesses" : ['
    position = 1
    for w in Witness.objects.all():
        if position != 1:
            jdata = jdata + ','
        jdata = jdata + '{"id": ' + jsonpickle.encode(w.witnessId) + '}'
        position += 1
    jdata = jdata + ']}'
    print jdata

    return HttpResponse(jdata, mimetype="application/json")

def getTokens(request):
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
    print jdata
    
    return HttpResponse(jdata, mimetype="application/json")
