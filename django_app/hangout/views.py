from django.views.generic import TemplateView

from hangout.models import Area


class HangoutSearchView(TemplateView):
    template_name = 'hangout/hangout_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['area_list'] = Area.objects.all()
        return context
