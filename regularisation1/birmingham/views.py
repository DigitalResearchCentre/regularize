from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from input.models import Token, Collation, Witness
from input.tables import ChangeTable
from input.forms import WitnessInputForm
from birmingham.models import Word, Versetext, Verse, WitnessBible
from django_tables2 import RequestConfig
from forms import ChooseTextForm
import pprint
import jsonpickle
import json
import httplib2

@csrf_exempt
def pickText(request, chapter, verse):
    # form = ChooseTextForm(request.POST or None, chapter="", verse="",\
    #                       initial="")

    # if request.method == "POST" and form.is_valid():
    #     print "here"
    # get chapter/verse texts to collate
    #if request.method == 'POST' and form.is_valid():
    #   chapter_choice = form.cleaned_data['chapter_choices']
    #  print chapter_choice
    # submit = request.POST.get('collate', None)
    # if submit and request.method == 'POST' and form.is_valid():
    #     verse_choice = form.cleaned_data['verse_choices']
    #     print verse_choice
    
    # get chapters of work1
    url = 'http://www.vmr.birmingham.ac.uk/api/work/1/'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    send = httplib2.Http()
    response, content = send.request(url, 'GET')
    # print response
    # pprint.pprint(content)

    jdata = json.loads(content)
    # print jdata

    chapters = [("0", "--")]
    chapters += [(str(data['id']), str(data['id']))\
               for data in jdata['chapters']]

    # get verses of chapter and set chapter to value previously selected
    if chapter != "0" and verse != "00":
        getText(chapter, verse)
        buildWitnesses(chapter, verse)
        collate(chapter, verse)
        return HttpResponseRedirect('/regularization/change/0/')
    elif chapter != "0":
        url = "http://www.vmr.birmingham.ac.uk/api/chapter/"
        url += chapter + "/"

        send = httplib2.Http()
        response, content = send.request(url, 'GET')
        jsonVerses = json.loads(content)
        # for data in jsonVerses['verses']:
        #     print data[0]
        verses = [("0", "--")]
        verses += [(str(data[0]), str(data[0]))\
               for data in jsonVerses['verses']]

        form = ChooseTextForm(request.POST or None, chapter=chapters,\
                              verse=verses, initial=chapter)
        return render_to_response('birmingham/pick_text.html',  {'form': form})

    form = ChooseTextForm(request.POST or None, chapter=chapters, verse="",\
                          initial="")
    
    return render_to_response('birmingham/pick_text.html',  {'form': form})

def buildWitnesses(chapter, verse):
    # print chapter
    # print verse
    # Witness.objects.all().delete()

    # get the verse/chapter to build the witnesses
    verse2 = Verse.objects.filter(chapter=chapter).filter(verse=verse)

    if verse2.count() == 1:
        # should only go once through loop (is only one)
        for v in verse2:
            # loop through the versetexts (manytomany) in the verse
            for vts in v.versetexts.all():
                # print vts.versetext
                words = Word.objects.filter(versetext=vts.versetext)
                content = ""
                pos = 1
                # loop through all words for this versetext
                for word in words:
                    w = Word.objects.filter(position=pos).filter(\
                                            versetext=vts.versetext)
                    # should be only one in that position of the versetext
                    for wt in w:
                        # if wt.text.isspace() == False:
                        if pos != 1:
                            content += " "
                        content += wt.text
                    pos += 1
                    
                filteredWitnesses = None
                filteredWitnesses = WitnessBible.objects.filter(\
                                        chapter=chapter).filter(\
                                        versetext=vts.versetext).filter(\
                                        content=content).filter(\
                                        verse=verse)
                if not filteredWitnesses:
                    # print "HERE!!!"
                    witness = WitnessBible.objects.create(chapter=chapter,\
                                            versetext=vts.versetext,\
                                            content=content,\
                                            verse=verse)
                    print content
        

def getText(chapter, verse):

    # Word.objects.all().delete()
    # Versetext.objects.all().delete()
    # Verse.objects.all().delete()
    
    # get chapter and verses for that chapter
    url = "http://www.vmr.birmingham.ac.uk/api/chapter/"
    url += chapter + "/"
    send = httplib2.Http()
    response, content = send.request(url, 'GET')
    chapterData = json.loads(content)
    
    # find url for verse desired
    for data in chapterData['verses']:
        if data[0] == verse:
            url = data[1]
            # print url
            
    # get versetexts
    response, content = send.request(url, 'GET')
    verseData = json.loads(content)
    # print verseTexts
    
    # filter the niput, as to not create duplicatesin the database
    filteredVerses = None
    filteredVerses = Verse.objects.filter(chapter=chapter).filter(\
                                        _id=verseData['id']).filter(\
                    short_identifier=verseData['short_identifier']).filter(\
                                        url=verseData['url']).filter(\
                                        verse=verse)
    if not filteredVerses:
        verse = Verse.objects.create(chapter=chapter,\
                                     _id=verseData['id'],\
                            short_identifier=verseData['short_identifier'],\
                            url = verseData['url'],\
                            verse = verse)
                                        
    # get all words from each versetexts
    for data in verseData['versetexts']:
        # save all versetexts
        if not filteredVerses:
            vt = Versetext.objects.create(versetext=data)
            print vt
            verse.versetexts.add(vt)
            verse.save()

        url = data
        response, content = send.request(url, 'GET')
        verseTexts = json.loads(content)
        for data2 in verseTexts['words']:
            url = data2
            response, content = send.request(url, 'GET')
            word = json.loads(content)

            # get rid of any None values (not allowed in db)
            if word['html'] == None:
                word['html'] = ""
            if word['index'] == None:
                word['index'] = ""
            if word['position'] == None:
                word['position'] = ""
            if word['tei'] == None:
                word['tei'] = ""
            if word['text'] == None:
                word['text'] = ""
            if word['url'] == None:
                word['url'] = ""
            if word['versetext'] == None:
                word['versetext'] = ""

            # filter the input, as to not create duplicates in the database
            filteredWords = None
            filteredWords = Word.objects.filter(html=word['html']).filter(\
                                         index=word['index']).filter(\
                                         position=word['position']).filter(\
                                         tei=word['tei']).filter(\
                                         text=word['text']).filter(\
                                         url=word['url']).filter(\
                                         versetext=word['versetext'])

            # if queryset is empty - add word to database
            if not filteredWords:
                w = Word.objects.create(html=word['html'],\
                                         index=word['index'],\
                                         position=word['position'],\
                                         tei=word['tei'],\
                                         text=word['text'],\
                                         url=word['url'],\
                                         versetext=word['versetext'])
                print w

# compute the collation from unload JSON
def collate(chapter, verse):
    Token.objects.all().delete()
    Witness.objects.all().delete()
    Collation.objects.all().delete()
    
    # get data from form, send to collatex engine and send resultant collation
    # onto the page that can change the collation
    url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    # creates form, if necessary
    form = WitnessInputForm()

    position = 1
    jdata = '{"witnesses" : ['
    for w in WitnessBible.objects.filter(chapter=chapter).filter(verse=verse):
        if position != 1:
            jdata = jdata + ','
        jdata = jdata + '{"id": ' + jsonpickle.encode(w.versetext) +\
            ', "content" : ' + jsonpickle.encode(w.content) + '}'
        position += 1
    jdata = jdata + ']}'
    # print jdata

    send = httplib2.Http()
    response, content = send.request(url, 'POST', jdata, headers)
    # print response
    # print content

    jdata = json.loads(content)
    print jdata

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
    # return HttpResponseRedirect('/regularization/change/0/')




        
