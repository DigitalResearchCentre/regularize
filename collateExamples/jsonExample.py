import json
import jsonpickle
import pprint

# JSON -> python object
objs = json.loads('{"alignment":[{"witness":"A","tokens":[{"t":"The","n":"the"},{"t":"black","n":"black"},null,null,null,{"t":"cat","n":"cat"}]},{"witness":"B","tokens":[{"t":"The","n":"the"},{"t":"black","n":"black"},null,{"t":"and","n":"and"},{"t":"white","n":"white"},{"t":"cat","n":"cat"}]},{"witness":"C","tokens":[{"t":"The","n":"the"},{"t":"black","n":"black"},null,{"t":"and","n":"and"},{"t":"green","n":"green"},{"t":"cat","n":"cat"}]},{"witness":"D","tokens":[{"t":"The","n":"the"},{"t":"black","n":"black"},null,{"t":"very","n":"very"},{"t":"special","n":"special"},{"t":"cat","n":"cat"}]},{"witness":"E","tokens":[{"t":"The","n":"the"},{"t":"black","n":"black"},{"t":"not","n":"not"},{"t":"very","n":"very"},{"t":"special","n":"special"},{"t":"cat","n":"cat"}]}]}')

# pretty printing of json object
# pprint.pprint(objs)

# go through the JSON object
# alignmnet is a dictionary of the witnesses,tokens pairs
for o in objs['alignment']:
    # print o['witness']
    # print o['tokens'][0]['t']
    
