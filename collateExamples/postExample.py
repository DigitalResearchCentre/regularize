import json
import pprint
import httplib2

url = 'http://127.0.0.1:8080/collatex-web-0.9.1-RC2/api/collate'
# url = 'http://gregor.middell.net/collatex/api/collate'

# content-type == sending type
# accept == type want back
#   could also be 'application/xml'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

jdata = json.dumps({"witnesses" : [{"id" : "A", "content" : "A black cat in a black basket" }, {"id" : "B", "content" : "A black cat in a black basket" }, {"id" : "C", "content" : "A striped cat in a black basket" }, {"id" : "D", "content" : "A striped cat in a white basket" }]})

# http post request
h = httplib2.Http()
response, content = h.request(url, 'POST', jdata, headers)
# print response
# print content

# go from json to python
objs = json.loads(content)
# pprint.pprint(objs)

# go through the JSON object
# alignmnet is a dictionary of the witnesses,tokens pairs
for data in objs['alignment']:
    # print object['witness']
    # print o['tokens'][0]['t']
    content = ""
    tokenList = []
    for token in data['tokens']:
        # print token['t']
        content = content + token['t'] + " "
        tokenList.append(token['t'])
    print content
    print tokenList



