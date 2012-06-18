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
