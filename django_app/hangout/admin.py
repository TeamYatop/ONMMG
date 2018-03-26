import requests
from django.contrib import admin
from django.core.exceptions import ValidationError

from hangout.form import HangoutForm, AreaForm, TagForm
from hangout.models import Hangout, Area


def request_address_2_coord_conversion(address):
    response = requests.get(
        'https://dapi.kakao.com/v2/local/search/address.json',
        headers={"Authorization": "KakaoAK d6c98772c22da8e2f99772ad89a32b40"},
        params={'query': address}
    )

    if response.status_code == 200:
        result = response.json()
    else:
        raise ValidationError('address conversion failed {}'.format(response.status_code))

    if result['meta']['total_count'] == 1:
        latitude = result['documents'][0]['y']
        longitude = result['documents'][0]['x']
    else:
        raise ValidationError('address need to have only one result: {}={}'.format(address,
                                                                                   result['meta']['total_count']))

    return latitude, longitude


class TagAdmin(admin.ModelAdmin):
    form = TagForm


class AreaAdmin(admin.ModelAdmin):
    form = AreaForm

    def save_model(self, request, obj, form, change):
        latitude, longitude = request_address_2_coord_conversion(form.cleaned_data['address'])
        obj.latitude = latitude
        obj.longitude = longitude
        return super(AreaAdmin, self).save_model(request, obj, form, change)


class HangoutAdmin(admin.ModelAdmin):
    form = HangoutForm

    def save_model(self, request, obj, form, change):
        latitude, longitude = request_address_2_coord_conversion(form.cleaned_data['address'])
        obj.latitude = latitude
        obj.longitude = longitude
        return super(HangoutAdmin, self).save_model(request, obj, form, change)


admin.site.register(Area, AreaAdmin)
# admin.site.register(Tag, TagAdmin)
admin.site.register(Hangout, HangoutAdmin)
