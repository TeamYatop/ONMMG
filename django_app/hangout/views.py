from django.views import View
from django.views.generic import ListView

from hangout.models import Hangout, Tag


class HangoutDefaultListView(ListView):
    template_name = 'hangout/hangout_list.html'

    def get_queryset(self):
        return Hangout.objects.all()

    def post(self, *args, **kwargs):
        return self.get(args, kwargs)


class HangoutListView(ListView):
    template_name = 'hangout/hangout_list.html'

    def get_queryset(self):
        if self.kwargs['tags']:
            tags = list()

            words = self.kwargs['tags'].split(',')
            for w in words:
                try:
                    tag = Tag.objects.get(word=w)
                except Tag.DoesNotExist:
                    pass
                else:
                    tags.append(tag)

            if tags:
                queryset = Hangout.objects.all()
                for tag in tags:
                    queryset = queryset.filter(tags__in=[tag])
                return queryset

            else:
                return Hangout.objects.none()

        else:
            return Hangout.objects.all()

    def post(self, *args, **kwargs):
        return self.get(args, kwargs)


class HangoutSearchView(View):
    def get(self, request):
        pass
