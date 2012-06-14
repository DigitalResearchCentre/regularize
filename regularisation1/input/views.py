from django.views.decorators.csrf import csrf_exempt
from forms import WitnessInputForm, RegularizationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Token, Witness, Collation
from tables import ChangeTable
from django_tables2 import RequestConfig
import pprint
import jsonpickle
import json
import httplib2

# compute the collation from unload JSON
def recollate():
    # get data from form, send to collatex engine and send resultant collation
    # onto the page that can change the collation
    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    # creates form, if necessary
    form = WitnessInputForm()

    position = 0
    jdata = '{"witnesses" : ['
    for w in Witness.objects.all():
        if position != 0:
            jdata = jdata + ','
        tokens = Token.objects.filter(witnessId=w.witnessId)
        jdata = jdata + '{"id": ' + jsonpickle.encode(w.witnessId) +\
            ', "tokens" : ['
        tokPos = 0
        for t in tokens:
            if tokPos != 0 and comma == True:
                jdata = jdata + ','
            comma = False
            token = tokens.filter(position=tokPos)
            for t in token:
                if t.content != '':
                    jdata = jdata + '{ "t" : ' + jsonpickle.encode(t.content)\
                        + '}'
                    comma = True
            tokPos = tokPos + 1
        jdata = jdata + ']}'
        position = position + 1
    jdata = jdata + ']}'
    # print jdata

    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)
    # print response
    # print content

    jdata = json.loads(content)
    # print jdata

    # DELETE EVERYTHING OUT OF DATABASE
    # TODO: JUST delete the ones that correspond to what recollating
    Token.objects.all().delete()
    Witness.objects.all().delete()
    Collation.objects.all().delete()

    c = Collation()
    c.save()
    for data in jdata['alignment']:
        content = ""
        pos = 0
        w = Witness()
        w.witnessId = data['witness']
        w.save() #must save before can add to manytomanyfield of witness
        for token in data['tokens']:
            if token != None:
                content = content + token['t'] + " "
                # must save before can add to m2mfield of witness
                t = Token.objects.create(content=token['t'], position=pos,\
                                         witnessId=data['witness'])
                w.tokenList.add(t)
                w.save()
            else:
                t = Token.objects.create(content="", position=pos,\
                                         witnessId=data['witness'])
                w.tokenList.add(t)
                w.save()
            pos = pos + 1
        w.content = content
        w.save() # changes to databases only happen with .save() is called
    c.witnessList.add(w)
    c.save()
                
    # change pages - to modifications page
    # redirect to page in urls.py
    return HttpResponseRedirect('/regularization/change/0/')

@csrf_exempt
def regularization(request):

    # get data from form, send to collatex engine and send resultant collation
    # onto the page that can change the collation
    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    # creates form, if necessary
    form = WitnessInputForm(request.POST or None)
    
    # getting data from form
    # POST means form has been submit
    if request.method == 'POST' and form.is_valid():
        witnessA = form.cleaned_data['witness_a']
        witnessB = form.cleaned_data['witness_b']
        witnessC = form.cleaned_data['witness_c']
        witnessD = form.cleaned_data['witness_d']
        witnessE = form.cleaned_data['witness_e']

        jdata = json.dumps({"witnesses" : [{"id" : "A", "content" : witnessA }, {"id" : "B", "content" : witnessB }, {"id" : "C", "content" : witnessC }, {"id" : "D", "content" : witnessD }, {"id" : "E", "content" : witnessE }]})

        send = httplib2.Http()
        response, content = send.request(url, 'POST', jdata, headers)

        # print response
        # print content
 
        jdata = json.loads(content)
        # print jdata

        # saving collation to database
        c = Collation()
        c.save()
        for data in jdata['alignment']:
            # print data['witness']
            # print data['tokens'][2]['t']
            content = ""
            pos = 0
            w = Witness()
            w.witnessId = data['witness']
            w.save() #must save before can add to manytomanyfield of witness
            for token in data['tokens']:
                if token != None:
                    print token['t']
                    content = content + token['t'] + " "
                    # t = Token(content=token['t'], position=pos,\
                    #           witnessId=data['witness'])
                    # t.save() 
                    # must save before can add to m2mfield of witness
                    t = Token.objects.create(content=token['t'],\
                                             original=token['t'],\
                                             position=pos,\
                                             witnessId=data['witness'])
                    w.tokenList.add(t)
                    w.save()
                else:
                    print ""
                    # t = Token(content="", position=pos,\
                    #           witnessId=data['witness'])
                    # t.save()
                    t = Token.objects.create(content="",\
                                             original="",\
                                             position=pos,\
                                             witnessId=data['witness'])
                    w.tokenList.add(t)
                    w.save()
                pos = pos + 1
            # print content
            w.content = content
            # print w
            w.save() # changes to databases only happen with .save() is called
        c.witnessList.add(w)
        c.save()
                
        # change pages - to modifications page
        # redirect to page in urls.py
        return HttpResponseRedirect('/regularization/change/0/')

    return render_to_response('input/regularisation.html', {'form': form})

@csrf_exempt
def change(request, pos):

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
            return HttpResponseRedirect(reverse('change', args=(position,)))

        submit = request.POST.get('back', None)
        if submit:
            # goto the last token/variant for regularization
            # TODO: 
            if int(pos) != 0:
                position = int(pos) - 1
                return HttpResponseRedirect(reverse('change', args=(position,)))

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

    # collation = Collation.objects.all()[:1]
    # witness = Witness.objects.reverse()[:1]

    return render_to_response('input/change.html', {'form': form})

@csrf_exempt
def show_original(request):

    if request.method == 'POST':
        submit = request.POST.get('done', None)
        if submit:
            return HttpResponseRedirect('/regularization/change/0/')

    # find the number of position in
    maxPos = 0
    for t in Token.objects.all():
        if t.position > maxPos:
            maxPos = t.position
            # print maxPos

    originalList = []
    # build list of dictionaries for table data
    for i in range(0, maxPos+1):
            
        dict = {}
        tokens = Token.objects.filter(position=i).distinct('content')
        allTokens = Token.objects.filter(position=i)
        content =''
        needComma = False
        for t in tokens:
            if needComma:
                content = content + ', '
            if t.content == "":
                # content = content + "None" + " "
                noComma = True
            else:
                for a in allTokens:
                    if a.content == t.content:
                        content = content + a.witnessId + ' '
                content = content + '(' + t.original + ') '
                needComma = True
        dict['originals'] = content
        originalList.append(dict)
        # print content
        #p rint originalList
    
    table = ChangeTable(originalList)
    
    return render_to_response('input/show_changes.html', {'table': table})


