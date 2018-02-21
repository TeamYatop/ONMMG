from django.db import models


class Tag(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return '#{}'.format(self.word)


class Hangout(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    tags = models.ManyToManyField(Tag, related_name='hangouts')

    def __str__(self):
        return 'Hangout({})'.format(self.title)
