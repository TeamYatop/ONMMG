import re
import string

from django.db import models
from django.utils.crypto import get_random_string

MAX_SLUG_LENGTH = 11
SLUG_LETTERS = string.ascii_letters + string.digits


class Area(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=140)
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)

    def __str__(self):
        return 'Area({})'.format(self.name)


class Tag(models.Model):
    word = models.CharField(max_length=50, unique=True)
    area = models.ForeignKey(Area, related_name='tag_set', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '#{}'.format(self.word)


class Hangout(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=140)
    description = models.CharField(max_length=140)
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    tags = models.ManyToManyField(Tag, related_name='hangouts', blank=True)
    slug = models.SlugField(max_length=MAX_SLUG_LENGTH, unique=True, blank=False)

    def __str__(self):
        return 'Hangout({})'.format(self.title)

    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.description)

        if not tags:
            return

        # todo : need clean up & code efficenty required
        # 디스크립션 내에서 태그의 변화를 인식하여 저장
        tags_a = set(t.word for t in self.tags.all())
        tags_b = set(tags)

        tags_union = tags_a.intersection(tags_b)

        added_tags = tags_b - tags_union
        remove_tags = tags_a - tags_union

        for t in added_tags:
            tag, tag_created = Tag.objects.get_or_create(word=t)
            self.tags.add(tag)

        for t in remove_tags:
            tag, tag_created = Tag.objects.get_or_create(word=t)
            self.tags.remove(tag)

    @classmethod
    def generate_unique_slug(cls):
        slug = get_random_string(MAX_SLUG_LENGTH, SLUG_LETTERS)
        if Hangout.objects.filter(slug=slug).exists():
            return cls.generate_unique_slug()
        else:
            return slug

    def slug_save(self):
        if not self.slug:
            self.slug = self.generate_unique_slug()

    def save(self, *args, **kwargs):
        self.slug_save()
        super(Hangout, self).save(args, kwargs)
        self.tag_save()
        super(Hangout, self).save(args, kwargs)
