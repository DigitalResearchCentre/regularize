class Token:
    def __init__(self, content, position, witnessId):
        self.content = content
        self.position = position
        self.witnessId = witnessId

class Witness:
    def __init__(self, id, content, tokenList):
        self.id = id
        self.content = content
        self.tokenList = tokenList

class Collation:
    def __init__(self, witnessList)
        self.witnessList = witnessList



