import requests
from django.contrib import admin
from django.core.exceptions import ValidationError

from hangout.form import HangoutForm
from hangout.models import Hangout, Tag


class HangoutAdmin(admin.ModelAdmin):
    form = HangoutForm

    def save_model(self, request, obj, form, change):
        params = {
            'query': form.cleaned_data['address']
        }
        response = requests.get(
            'https://dapi.kakao.com/v2/local/search/address.json',
            headers={"Authorization": "KakaoAK a84ee72870c8ac12a6c3aca72a82030f"},
            params=params
        )
        if response.status_code == 200:
            result = response.json()
            if result['meta']['total_count'] == 1:
                obj.latitude = result['documents'][0]['y']
                obj.longitude = result['documents'][0]['x']
                return super(HangoutAdmin, self).save_model(request, obj, form, change)
            else:
                raise ValidationError('address has multiple results {}'.format(result['meta']['total_count']))
        else:
            raise ValidationError('address conversion failed {}'.format(response.status_code))


admin.site.register(Hangout, HangoutAdmin)
admin.site.register(Tag)
