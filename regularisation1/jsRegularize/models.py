from django.db import models

class Modification(models.Model):
    userId = models.CharField(max_length=100)
    action = models.CharField(max_length=200)
    dateTime = models.DateTimeField()

class Rule(models.Model):
    ruleID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    user = models.ManyToManyField(Modification)
    #user = models.CharField(max_length=20)
    scope = models.CharField(max_length=20)
    regularization_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    lemma = models.CharField(max_length=20)

class RuleSet(models.Model):
    name = models.CharField(max_length=100)
    ruleSetID = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    userId = models.CharField(max_length=50)
    rules = models.ManyToManyField(Rule)

class Line(models.Model):
    witnessId = models.CharField(max_length=10)
    content = models.CharField(max_length=1000)
    number = models.IntegerField()

class SelectedWitnesses(models.Model):
    userId = models.CharField(max_length=50)
    urn = models.CharField(max_length=100)
    witnesses = models.CharField(max_length=25000)
