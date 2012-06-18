from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from input.models import Token, Witness, Collation
from input.tables import ChangeTable
from birmingham.models import Word
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
       collateText(chapter, verse)
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

def collateText(chapter, verse):
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
    
    # get all words from each versetexts
    for data in verseData['versetexts']:
        url = data
        response, content = send.request(url, 'GET')
        verseTexts = json.loads(content)
        for data2 in verseTexts['words']:
            url = data2
            response, content = send.request(url, 'GET')
            word = json.loads(content)
            
                # if data3['html'] == None:
                #     data3['html'] = ""
            w = Word.objects.create(html=word['html'],\
                                         index=word['index'],\
                                         position=word['position'],\
                                         tei=word['tei'],\
                                         text=word['text'],\
                                         url=word['url'],\
                                         versetext=word['versetext'])
            print w
                                             
                
        
