from django.views import generic

from hangout.models import Hangout


class HangoutListView(generic.ListView):
    # model = Hangout
    template_name = 'hangout/hangout_list.html'

    def get_queryset(self):
        return Hangout.objects.all()
