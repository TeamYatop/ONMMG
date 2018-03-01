from django.shortcuts import get_object_or_404
from django.views import generic

from hangout.models import Hangout, Tag


class HangoutDefaultListView(generic.ListView):
    template_name = 'hangout/hangout_list.html'

    def get_queryset(self):
        return Hangout.objects.all()


class HangoutListView(generic.ListView):
    template_name = 'hangout/hangout_list.html'

    def get_queryset(self):
        if self.kwargs['tags']:
            tags = self.kwargs['tags'].split(',')
            tags = [Tag.objects.get(word=t) for t in tags]
            queryset = Hangout.objects.all()
            for tag in tags:
                queryset = queryset.filter(tags__in=[tag])
            return queryset
        else:
            return Hangout.objects.all()

    def post(self, *args, **kwargs):
        return self.get(args, kwargs)
