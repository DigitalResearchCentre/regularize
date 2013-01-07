from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from models import Rule, RuleSet, Modification, Alignment
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from itertools import chain
from django.template import RequestContext

import pprint
import jsonpickle
import json
import httplib2
import HTMLParser

def regularization(request):
    # request should contain json with username and urn

    #urn = "urn:det:TCUSASK:CTP2:entity=MI:Tale=MI:Line=IR"
    #userName = "user@mail.usask.ca"

    urn = request.GET.get('urn', '')
    userName = request.GET.get('username', '')
    returnUrl = request.GET.get('page', '')

    witData = getWitnessData(urn)
    witnesses = json.loads(witData[0])
    request.session['data'] = witnesses['witnesses']
    images = witData[1]
    ruleSets = json.loads(getRuleSets(userName, urn, witData))
    ruleSetName = 'default'

    urlCollation = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    filteredRuleSet = RuleSet.objects.filter(userId=userName).filter(\
                                                        appliesTo=urn).filter(name=ruleSetName)
    if not filteredRuleSet:
        rs = RuleSet()
        rs.userId = userName
        rs.appliesTo = urn
        rs.name = ruleSetName
        rs.save()
        ruleSet = '{}'
    else:
        for rs in ruleSets['ruleSets']:
            if rs['name'] == "default":
                ruleSet = rs

    witnesses = checkDuplicateWitnesses(witnesses['witnesses'])
    witnesses = json.dumps({'witnesses': witnesses})
    ruleSet = json.dumps({'ruleSet': ruleSet})
        
    send = httplib2.Http()
    response, content = send.request(urlCollation, 'POST', witnesses, headers)

    return render_to_response('jsRegularize/collate_interface.html', {"userName" : userName, "urn" : urn, "witnessesTokens" : content, "witnessesLines": witnesses, "ruleSetName": ruleSetName, "ruleSet": ruleSet, "position": 0, "images": images, "returnUrl": returnUrl}, context_instance=RequestContext(request))

def collationInterface(request):
    urlCollation = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    if request.session.get('data'):
        jdata = request.session.pop('data')
        jdata = json.loads(jdata)
        request.session['data'] = jdata['witnesses']
        userName = jdata['userName']
        urn = jdata['urn']
        ruleSetName = "default"
        returnUrl = jdata['returnUrl']
        witnesses = jdata['witnesses']
        images = json.dumps({'images': jdata['images']})
        ruleSets = jdata['ruleSets']
        #print ruleSets
        #ruleSet = json.dumps({'ruleSet': jdata['ruleSet']})
        #witnesses = json.dumps({'witnesses': jdata['witnesses'][0]})
        #images = json.dumps({'images': jdata['images'][0]})

        filteredRuleSet = RuleSet.objects.filter(userId=userName).filter(\
                                                        appliesTo=urn).filter(name=ruleSetName)
        if not filteredRuleSet:
            rs = RuleSet()
            rs.userId = userName
            rs.appliesTo = urn
            rs.name = ruleSetName
            rs.save()
            ruleSet = '{}'
        else:
            for rs in ruleSets:
                if rs['name'] == "default":
                    ruleSet = rs

        witnesses = checkDuplicateWitnesses(witnesses)
        witnesses = json.dumps({'witnesses': witnesses})
        ruleSet = json.dumps({'ruleSet': ruleSet})
        
        send = httplib2.Http()
        response, content = send.request(urlCollation, 'POST', witnesses, headers)
        #return HttpResponse("OK")
        
        return render_to_response('jsRegularize/collate_interface.html', {"userName" : userName, "urn" : urn, "witnessesTokens" : content, "witnessesLines": witnesses, "ruleSetName": ruleSetName, "ruleSet": ruleSet, "position": 0, "images": images, "returnUrl": returnUrl}, context_instance=RequestContext(request))

def checkDuplicateWitnesses(witnesses):
    w1Num = 0
    for w1 in witnesses:
        w2Num = 0
        for w2 in witnesses:
            if w1['id'] == w2['id'] and w1Num != w2Num:
                witnesses.pop(w2Num)
            w2Num = w2Num + 1
        w1Num = w1Num + 1

    return witnesses
    
def getWitnessData(urn):
    parser = HTMLParser.HTMLParser()
    jdata = '{"witnesses":['
    jdata2 = '{"images":['
    number = 0

    urlDoc = "http://textualcommunities.usask.ca/drc/api/urn/" + urn + "/"
    urlText = "http://textualcommunities.usask.ca/drc/api/text/"
    urlDet = "http://textualcommunities.usask.ca/drc/api/det/"

    ## comment out if urls start working again
    #jdata = getTestData()
    #return jdata

    send = httplib2.Http()
    response, content = send.request(urlDoc, 'GET')

    documentInfo = json.loads(content)

    length = len(documentInfo['hastextof'])
    #print length
    numberLength = 0
    for witness in documentInfo['hastextof']:
        if(number == length):
            break
        numberLength = numberLength + 1
        #print numberLength
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
                jdata2 = jdata2 + ','
            #jdata = jdata + '{"urn": ' + jsonpickle.encode(det['urn']) + ','
            #print det['urn']
            
            _id = det['urn'].split("document=")[1]
            _id = "".join(_id)
            _id = _id.split(":")[0]
            _id = "".join(_id)
            #jdata = jdata + '"id": ' + jsonpickle.encode(_id) + ','
            jdata = jdata + '{"id": ' + jsonpickle.encode(_id) + ','
            jdata2 = jdata2 + '{"id": ' + jsonpickle.encode(_id) + ','
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
            #x = x.split("<lb n=\"\">")
            # x = "".join(x)
            x = x.split("</lb>")
            x = "".join(x)
            x = x.split("<hi rend=\"unex\">")
            x = "".join(x)
            x = x.split("<hi rend=\"sup\">")
            x = "".join(x)
            x = x.split("<hi rend=\"ud\">")
            x = "".join(x)
            x = x.split("\"")
            x = "".join(x)
            x = x.split("<lb n=/>")
            x = "".join(x)
            # x = x.split("&lt;gap extent=&quot;")
            # if(len(x) >= 2):
            #     x[1] = x[1][1:]
            # x = "".join(x)
            # x = x.split("&quot;&gt;&lt;/gap&gt;")
            # x = "".join(x)
            x = x.replace("&amp;", "&")
            x = parser.unescape(x)
            jdata = jdata + '"content": ' + jsonpickle.encode(x) + '}'
            jdata2 = jdata2 + '"url": ' + jsonpickle.encode(det['img']) + '}'
            # print x

            number = number + 1
            #print text['istextin']
        except ValueError:
            print "valueError: " + str(text['istextin'])

    jdata = jdata + ']}'
    jdata2 = jdata2 + ']}'

    dataList = []
    dataList.append(jdata)
    dataList.append(jdata2)
    #pprint.pprint(jdata)

    return dataList

@csrf_exempt
def postSelectedWitnesses(request):
    if request.is_ajax():
       if request.method == 'POST':
           request.session['selectedWitnesses'] = request.raw_post_data

    return HttpResponse("OK")

def chooseRuleSetsInterface(request):
    if request.session.get('selectedWitnesses'):
        jdata = request.session.pop('selectedWitnesses')
        jdata = json.loads(jdata)
        userName = jdata['userName']
        urn = jdata['urn']
        returnUrl = jdata['returnUrl']
        # TODO: May have to change this line
        witnesses = '{"witnesses":[' + jsonpickle.encode(jdata['witnesses']) + ']}'
        images = '{"images": [' + jsonpickle.encode(jdata['images']) + ']}'
        jdata = getRuleSets(userName, urn, jdata)
        return render_to_response('jsRegularize/chooseRuleSets_interface.html', {"userName" : userName, "urn" : urn, "witnesses" : witnesses, "ruleSetData": jdata, "images": images, "returnUrl": returnUrl}, context_instance=RequestContext(request))
    else:
       return HttpResponse(status=500)

def getRuleSets(userName, urn, jdata):
        filteredRuleSets = RuleSet.objects.filter(appliesTo=urn).filter(userId=userName)

        jdata = '{ "ruleSets": ['
        if filteredRuleSets:
            ruleSetNum = 0
            for rs in filteredRuleSets:
                if(ruleSetNum != 0):
                    jdata = jdata + ","
                jdata = jdata + '{"name": ' + jsonpickle.encode(rs.name) + ','
                jdata = jdata + '"appliesTo": ' + jsonpickle.encode(rs.appliesTo) + ','
                jdata = jdata + '"userId": ' + jsonpickle.encode(rs.userId) + ','
                jdata = jdata + '"rules": ['
                ruleNum = 0
                for r in rs.rules.all():
                    if(ruleNum != 0):
                        jdata = jdata + ","
                    jdata = jdata + '{"appliesTo": ' + jsonpickle.encode(r.appliesTo) + ','
                    jdata = jdata + '"action": ' + jsonpickle.encode(r.action) + ','
                    jdata = jdata + '"scope": ' + jsonpickle.encode(r.scope) + ','
                    jdata = jdata + '"token": ' + jsonpickle.encode(r.token) + ','
                    jdata = jdata + '"modifications": ['
                    modificationNum = 0
                    for m in r.modifications.all():
                        if(modificationNum != 0):
                            jdata = jdata + ","
                        jdata = jdata + '{"userId": ' + jsonpickle.encode(m.userId) + ','
                        jdata = jdata + '"modification_type": ' + \
                            jsonpickle.encode(m.modification_type) + ','
                        jdata = jdata + '"dateTime": ' + jsonpickle.encode(m.dateTime) + '}'
                        modificationNum = modificationNum + 1
                    jdata = jdata + ']}'
                    ruleNum = ruleNum + 1
                jdata = jdata + '],'
                jdata = jdata + '"alignments": ['
                alignNum = 0
                for a in rs.alignments.all():
                    if(alignNum != 0):
                        jdata = jdata + ","
                    jdata = jdata + '{"appliesTo":' + jsonpickle.encode(a.appliesTo) + ','
                    jdata = jdata + '"witnessId": ' + jsonpickle.encode(a.witnessId) + ','
                    jdata = jdata + '"isForward": ' + jsonpickle.encode(a.isForward) + ','
                    jdata = jdata + '"isMove": ' + jsonpickle.encode(a.isMove) + ','
                    jdata = jdata + '"token": ' + jsonpickle.encode(a.token) + ','
                    jdata = jdata + '"numPos": ' + jsonpickle.encode(a.numPos) + ','
                    jdata = jdata + '"position": ' + jsonpickle.encode(a.position) + ','
                    jdata = jdata + '"context": ' + jsonpickle.encode(a.context) + ','
                    jdata = jdata + '"modifications": ['
                    modificationNum = 0
                    for m in a.modifications.all():
                        if(modificationNum != 0):
                            jdata = jdata + ","
                        jdata = jdata + '{"userId": ' + jsonpickle.encode(m.userId) + ','
                        jdata = jdata + '"modification_type": ' + \
                            jsonpickle.encode(m.modification_type) + ','
                        jdata = jdata + '"dateTime": ' + jsonpickle.encode(m.dateTime) + '}'
                        modificationNum = modificationNum + 1
                    jdata = jdata + ']}'
                    alignNum = alignNum + 1
                jdata = jdata + ']}'
                ruleSetNum = ruleSetNum + 1
        jdata = jdata + ']}'
        #print jdata
        return jdata

@csrf_exempt
def postSelectedRuleSets(request):
    if request.is_ajax():
        if request.method == 'POST':
            request.session['selectedRuleSets'] = request.raw_post_data
            request.session['data'] = request.raw_post_data
            
    return HttpResponse("OK")

@csrf_exempt
def postNewRule(request):
    #Modification.objects.all().delete()
    #Rule.objects.all().delete()
    
    if request.is_ajax():
        if request.method == 'POST':
            jdata = json.loads(request.raw_post_data)
            print jdata

            filteredRuleSet = RuleSet.objects.filter(userId=jdata['userName']).filter(\
                                appliesTo=jdata['urn']).filter(name=jdata['ruleSetName'])

            if filteredRuleSet and filteredRuleSet.count() == 1:
                filteredModifications = Modification.objects.filter(userId=jdata['userName']).filter(\
                    modification_type=jdata['rules'][0]['modifications'][0]['modification_type']).filter(\
                    dateTime=jdata['rules'][0]['modifications'][0]['dateTime'])
                
                found = False
                for rule in filteredRuleSet[0].rules.all():
                    if (rule.appliesTo == jdata['urn'] and rule.action == \
                        jdata['rules'][0]['action'] and rule.scope == jdata['rules'][0]['scope'] \
                        and rule.token == jdata['rules'][0]['token']):
                        found = True
                        
                if not filteredModifications and not found:
                    m = Modification()
                    m.userId = jdata['userName']
                    m.modification_type = jdata['rules'][0]['modifications'][0]['modification_type']
                    m.dateTime = jdata['rules'][0]['modifications'][0]['dateTime']
                    m.save()
                    
                    r = Rule()
                    r.appliesTo = jdata['urn']
                    r.action = jdata['rules'][0]['action']
                    r.scope = jdata['rules'][0]['scope']
                    r.token = jdata['rules'][0]['token']
                    r.save()
                    r.modifications.add(m)
                    filteredRuleSet[0].rules.add(r)
                else:
                    print "error: filteredModifications OR filteredRules"
            else:
                print "error: filteredRuleSet"
                
    return HttpResponse("OK")

@csrf_exempt
def changeRules(request):
    if request.is_ajax():
       if request.method == 'POST':
           jdata = json.loads(request.raw_post_data)
           print jdata

           filteredRuleSet = RuleSet.objects.filter(userId=jdata['userName']).filter(\
                                appliesTo=jdata['urn']).filter(name=jdata['ruleSetName'])

           if filteredRuleSet and filteredRuleSet.count() == 1:
               for modification in jdata['rules']:
                    found = False
                    for rule in filteredRuleSet[0].rules.all():
                        # filteredModifications = Modification.objects.filter(userId=jdata['userName']\
                        #                 ).filter(modification_type=jdata['modification']['modifications']\
                        #                 [0]['modification_type']).filter(dateTime=jdata['rules'][0]\
                        #                 ['modifications'][0]['dateTime'])
                        if (rule.appliesTo == jdata['urn'] and rule.action == \
                            modification['action'] and rule.scope == modification['scope'] \
                            and rule.token == modification['token']):
                            found = True
                            modifiedRule = rule
                        
                    if found:
                        m = Modification()
                        m.userId = jdata['userName']
                        m.modification_type = modification['modifications'][-1]['modification_type']
                        m.dateTime = modification['modifications'][-1]['dateTime']
                        m.save()
                        modifiedRule.modifications.add(m)
                        
                        modify = modification['modifications'][-1]['modification_type']
                        print modify
                        if modify != 'delete':
                            modify = modify.split("modify(")
                            modify = "".join(modify)
                            modify = modify.split(")")
                            modify = "".join(modify)
                            modify = modify.split(",")
                            modType = modify[0]
                            modFrom = modify[1]
                            modTo = modify[2]

                            if(modType == 'scope'):
                                modifiedRule.scope = modTo

                            if(modType == 'reg_this'):
                                modifiedRule.token = modTo
                                regTo = modifedRule.action.split(",")[-1]
                                regTo = "".join(regTo)
                                regTo = regTo.split(")")[0]
                                regTo = "".join(regTo)
                                modifiedRule.action = "regularize(" + modTo + "," + regTo + ")";

                            if(modType == 'reg_to'):
                                regThis = modifieRule.action.split(",")[0]
                                regThis = "".join(regThis)
                                regThis = regThis.split("(")[-1]
                                regThis = "".join(regThis)
                                modifedRule.action = "regularize(" + regThis + "," + modTo + ")";
                                
                            modifiedRule.save()
                        
    return HttpResponse("OK")

@csrf_exempt
def postRecollate(request):
    if request.is_ajax():
       if request.method == 'POST':
           request.session['recollate'] = request.raw_post_data
           #print request.raw_post_data
           
    return HttpResponse("OK")

def sendRecollate(request):
    if request.session.get('recollate'):
        jdata = request.session.pop('recollate')
        #print jdata
        #jdata2 = json.loads(jdata)
        
    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)
    #print response
    #print content

    return HttpResponse(content, mimetype="application/json")

def getBaseTokens(request):
    #jdata = getTestData()
    #print jdata
    
    if request.session.get('data'):
        jdata = request.session.pop('data')
        request.session['data'] = jdata
        jdata = checkDuplicateWitnesses(jdata)
        jdata = json.dumps({'witnesses': jdata})
    
        url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        send = httplib2.Http()
        response, content = send.request(url, 'POST', jdata, headers)
        #print content
        return HttpResponse(content, mimetype="application/json")

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

@csrf_exempt
def postNewAlign(request):
    if request.is_ajax():
        if request.method == 'POST':
            jdata = json.loads(request.raw_post_data)
            #print jdata

            filteredRuleSet = RuleSet.objects.filter(userId=jdata['userName']).filter(\
                                appliesTo=jdata['urn']).filter(name=jdata['ruleSetName'])

            if filteredRuleSet and filteredRuleSet.count() == 1:
                for newAlign in jdata['alignments']:
                    found = False
                    print newAlign
                    for align in filteredRuleSet[0].alignments.all():
                        if (align.appliesTo == jdata['urn'] and align.appliesTo == \
                            newAlign['appliesTo'] and align.witnessId == \
                            newAlign['witnessId'] and align.isForward == \
                            newAlign['isForward'] and align.isMove == \
                            newAlign['isMove'] and align.numPos == \
                            newAlign['numPos'] and align.token == \
                            newAlign['position'] and align.position == \
                            newAlign['token'] and align.context == \
                            newAlign['context']):
                            print "hereFound"
                            found = True
                        
                    if not found:
                        print "here"
                        m = Modification()
                        m.userId = jdata['userName']
                        m.modification_type = newAlign['modifications'][0]\
                            ['modification_type']
                        m.dateTime = newAlign['modifications'][0]['dateTime']
                        m.save()

                        a = Alignment()
                        a.appliesTo = jdata['urn']
                        a.witnessId = newAlign['witnessId']
                        a.isMove = newAlign['isMove']
                        a.isForward = newAlign['isForward']
                        a.token = newAlign['token']
                        a.numPos = newAlign['numPos']
                        a.context = newAlign['context']
                        a.position = newAlign['position']
                        a.save()
                        print a.witnessId
                        a.modifications.add(m)
                        filteredRuleSet[0].alignments.add(a)
            else:
                print "error: filteredRuleSet"
                
    return HttpResponse("OK")

@csrf_exempt
def changeAligns(request):
    if request.is_ajax():
       if request.method == 'POST':
           jdata = json.loads(request.raw_post_data)
           print jdata

           filteredRuleSet = RuleSet.objects.filter(userId=jdata['userName']).filter(\
                                appliesTo=jdata['urn']).filter(name=jdata['ruleSetName'])

           if filteredRuleSet and filteredRuleSet.count() == 1:
               for modification in jdata['alignments']:
                    found = False
                    for align in filteredRuleSet[0].alignments.all():
                       if (align.appliesTo == jdata['urn'] and align.appliesTo == \
                        modification['appliesTo'] and align.witnessId == \
                        modification['witnessId'] and align.isForward == \
                        modification['isForward'] and align.isMove == \
                        modification['isMove'] and align.numPos == \
                        modification['numPos'] and align.token == \
                        modification['token'] and align.position == \
                        modification['position'] and align.context == \
                        modification['context']):
                           modifications = align.modifications.all()
                           number = 1
                           for modificationIn in modifications:
                               if(number == len(modifications) and modificationIn.modification_type != \
                                  'delete'):
                                   print "here"
                                   m = Modification()
                                   m.userId = jdata['userName']
                                   m.modification_type = modification['modifications'][-1]\
                                       ['modification_type']
                                   m.dateTime = modification['modifications'][-1]['dateTime']
                                   m.save()
                                   align.modifications.add(m)
                               number = number + 1
                        
    return HttpResponse("OK")

@csrf_exempt
def deleteRuleSet(request):
    if request.is_ajax():
       if request.method == 'POST':
           jdata = json.loads(request.raw_post_data)
           print jdata

           filteredRuleSet = RuleSet.objects.filter(userId=jdata['userName']).filter(\
                                appliesTo=jdata['urn']).filter(name=jdata['ruleSetName']).delete()

    return HttpResponse("OK")
