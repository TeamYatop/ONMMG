import re

from django.db import models


class Tag(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '#{}'.format(self.word)


class Hangout(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=140)
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    tags = models.ManyToManyField(Tag, related_name='hangouts', blank=True)

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

    def save(self, *args, **kwargs):
        super(Hangout, self).save(args, kwargs)
        self.tag_save()
        super(Hangout, self).save(args, kwargs)
