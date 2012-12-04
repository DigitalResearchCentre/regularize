from django.db import models

class Modification(models.Model):
    userId = models.CharField(max_length=100)
    modification_type = models.CharField(max_length=300)
    dateTime = models.CharField(max_length=100)

class Rule(models.Model):
    ruleID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    modifications = models.ManyToManyField(Modification)
    scope = models.CharField(max_length=20)
    token = models.CharField(max_length=100)

class Alignment(models.Model):
    alignmentID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    witnessId = models.CharField(max_length=100)
    context = models.CharField(max_length=1000)
    isMove = models.BooleanField()
    isForward = models.BooleanField()
    token = models.CharField(max_length=200)
    numPos = models.IntegerField()
    position = models.IntegerField()
    modifications = models.ManyToManyField(Modification)

class RuleSet(models.Model):
    name = models.CharField(max_length=100)
    ruleSetID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    userId = models.CharField(max_length=50)
    rules = models.ManyToManyField(Rule)
    alignments = models.ManyToManyField(Alignment)
