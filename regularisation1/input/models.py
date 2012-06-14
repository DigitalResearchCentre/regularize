from django.db import models

class Token(models.Model):
    content = models.CharField(max_length=200)
    original = models.CharField(max_length=200)
    position = models.IntegerField()
    witnessId = models.CharField(max_length=20)

    def __unicode__(self):
        return self.content

class Witness(models.Model):
    tokenList = models.ManyToManyField(Token)
    content = models.CharField(max_length=200)
    witnessId = models.CharField(max_length=20)

    def __unicode__(self):
        return self.content

class Collation(models.Model):
    witnessList = models.ManyToManyField(Witness)
