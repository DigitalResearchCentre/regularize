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

class RuleSet(models.Model):
    name = models.CharField(max_length=100)
    ruleSetID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    userId = models.CharField(max_length=50)
    rules = models.ManyToManyField(Rule)
    # alignments = models.ManyToManyField(Alignment)

class Alignment(models.Model):
    alignmentID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    position = models.IntegerField()
    isForward = models.BooleanField()
    token = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    realignNum = models.IntegerField()
