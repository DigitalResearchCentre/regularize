from django.db import models

class Word(models.Model):
    html = models.CharField(max_length=200)
    index = models.CharField(max_length=200)
    position = models.CharField(max_length=20)
    tei = models.CharField(max_length=500)
    text = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    versetext = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text

class Versetext(models.Model):
    versetext = models.CharField(max_length=200)

    def __unicode__(self):
        return self.versetext

class Verse(models.Model):
    chapter = models.CharField(max_length=100)
    verse = models.CharField(max_length=100)
    _id = models.CharField(max_length=20)
    short_identifier = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    versetexts = models.ManyToManyField(Versetext)

    def __unicode__(self):
        return self._id

class WitnessBible(models.Model):
    chapter = models.CharField(max_length=100)
    verse = models.CharField(max_length=100)
    versetext = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)

class Rule(models.Model):
    _id = models.CharField(max_length=100)
    appliesTo = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    user = models.CharField(max_length=20)
    scope = models.CharField(max_length=20)
    regularization_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    token = models.CharField(max_length=20)
    lemma = models.CharField(max_length=20)
    json = models.CharField(max_length=1000)
