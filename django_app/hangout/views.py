from django.shortcuts import get_object_or_404
from django.views import generic

from hangout.models import Hangout, Tag


class HangoutListView(generic.ListView):
    template_name = 'hangout/hangout_list.html'

    # all
    # def get_queryset(self):
    #     return Hangout.objects.all()

    # filter one
    # def get_queryset(self):
    #     if self.request.GET.get('tags'):
    #         tags = self.request.GET.get('tags')
    #         tag = Tag.objects.filter(word=tags)
    #         return Hangout.objects.filter(tags__in=tag)
    #     else:
    #         return Hangout.objects.all()

    # filter more then one
    def get_queryset(self):
        if self.request.GET.get('tags'):
            tags = self.request.GET.get('tags').split(',')
            tags = [Tag.objects.get(word=t) for t in tags]

            queryset = Hangout.objects.all()
            for tag in tags:
                queryset = queryset.filter(tags__in=[tag])
            return queryset
        else:
            return Hangout.objects.all()
