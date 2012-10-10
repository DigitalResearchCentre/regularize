from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from models import Rule, RuleSet, Modification
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

    return HttpResponse("OK")

def chooseRuleSetsInterface(request):
    if request.session.get('selectedWitnesses'):
        jdata = request.session.pop('selectedWitnesses')
        jdata = json.loads(jdata)
        userName = jdata['userName']
        urn = jdata['urn']
        # TODO: May have to change this line
        witnesses = '{"witnesses":[' + jsonpickle.encode(jdata['witnesses']) + ']}'

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
                jdata = jdata + ']}'
            ruleSetNum = ruleSetNum + 1

        jdata = jdata + ']}'
        #print jdata
        
        return render_to_response('jsRegularize/chooseRuleSets_interface.html', {"userName" : userName, "urn" : urn, "witnesses" : witnesses, "ruleSetData": jdata}, context_instance=RequestContext(request))

@csrf_exempt
def postSelectedRuleSets(request):
    if request.is_ajax():
        if request.method == 'POST':
            request.session['selectedRuleSets'] = request.raw_post_data
            
    return HttpResponse("OK")

def loadRegularizationInterface(request):
    # RuleSet.objects.all().delete()
    
    urlCollation = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    if request.session.get('selectedRuleSets'):
        jdata = request.session.pop('selectedRuleSets')
        jdata = json.loads(jdata)
        userName = jdata['userName']
        urn = jdata['urn']
        ruleSetName = jdata['ruleSetName']
        ruleSet = json.dumps({'ruleSet': jdata['ruleSet']})
        witnesses = json.dumps({'witnesses': jdata['witnesses'][0]})

        filteredRuleSet = RuleSet.objects.filter(userId=userName).filter(\
                                                        appliesTo=urn).filter(name=ruleSetName)
        if not filteredRuleSet:
            rs = RuleSet()
            rs.userId = userName
            rs.appliesTo = urn
            rs.name = ruleSetName
            rs.save()

        send = httplib2.Http()
        response, content = send.request(urlCollation, 'POST', witnesses, headers)
        
        return render_to_response('jsRegularize/collate_interface.html', {"userName" : userName, "urn" : urn, "witnessesTokens" : content, "witnessesLines": witnesses, "ruleSetName": ruleSetName, "ruleSet": ruleSet, "position": 0}, context_instance=RequestContext(request))

@csrf_exempt
def postNewRule(request):
    #Modification.objects.all().delete()
    #Rule.objects.all().delete()
    
    if request.is_ajax():
        if request.method == 'POST':
            jdata = json.loads(request.raw_post_data)
            #print jdata

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
def postEntireReg(request):
    if request.is_ajax():
       if request.method == 'POST':
           request.session['entireReg'] = request.raw_post_data

    return HttpResponse("OK")

def viewEntireReg(request):
    if request.session.get('entireReg'):
        jdata = request.session.pop('entireReg')
        #print jdata

    return render_to_response('jsRegularize/view_reg.html', {"witnesses": jdata}, context_instance=RequestContext(request))

def reloadRegularizationInterface(request):
    if request.session.get('entireReg'):
        jdata = request.session.pop('entireReg')
        jdata = json.loads(jdata)
        userName = jdata['userName']
        urn = jdata['urn']
        ruleSetName = jdata['ruleSetName']
        position = jdata['position']
        ruleSet = json.dumps({'ruleSet': jdata['ruleSet']})
        witnesses = json.dumps({'witnesses': jdata['witnesses'][0]})
        content = json.dumps(jdata['witnessesTokens'])

    return render_to_response('jsRegularize/collate_interface.html', {"userName" : userName, "urn" : urn, "witnessesTokens" : content, "witnessesLines": witnesses, "ruleSetName": ruleSetName, "ruleSet": ruleSet, "position": position}, context_instance=RequestContext(request))

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

    return HttpResponse("OK")

def sendRecollate(request):
    if request.session.get('recollate'):
        jdata = request.session.pop('recollate')

    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)
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
