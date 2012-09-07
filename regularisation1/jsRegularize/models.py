from django.db import models

class Token(models.Model):
    content = models.CharField(max_length=200)
    normalized = models.CharField(max_length=200)
    position = models.IntegerField()
    witnessId = models.CharField(max_length=500)

    def __unicode__(self):
        return self.content

class Witness(models.Model):
    tokenList = models.ManyToManyField(Token)
    content = models.CharField(max_length=200)
    witnessId = models.CharField(max_length=500)

    def __unicode__(self):
        return self.content

class Collation(models.Model):
    witnessList = models.ManyToManyField(Witness)

class Rule(models.Model):
    ruleID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    user = models.CharField(max_length=20)
    scope = models.CharField(max_length=20)
    regularization_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    lemma = models.CharField(max_length=20)

class Line(models.Model):
    witnessId = models.CharField(max_length=10)
    content = models.CharField(max_length=1000)
    number = models.IntegerField()
