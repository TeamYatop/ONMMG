from django.db import models, transaction


class Tag(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return '#{}'.format(self.word)


class Hangout(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    tags = models.ManyToManyField(Tag, related_name='hangouts', blank=True)

    def __str__(self):
        return 'Hangout({})'.format(self.title)
