from django.views import generic

from hangout.models import Hangout


# Create your views here.

class HangoutListView(generic.ListView):
    def get_queryset(self):
        return Hangout.objects.all()
