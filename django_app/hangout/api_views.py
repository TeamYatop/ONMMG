from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from hangout.models import Hangout, Tag, Area
from hangout.serializers import HangoutSerializer


@api_view()
def hangout_list(request):
    hangouts = Hangout.objects.all()
    serializer = HangoutSerializer(hangouts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view()
def hangout_detail(request, slug):
    try:
        hangout = Hangout.objects.get(slug=slug)
    except Hangout.DoesNotExist:
        return HttpResponse(status=404)
    else:
        serializer = HangoutSerializer(hangout)
        return JsonResponse(serializer.data)


@api_view()
def hangout_search_by_tags(request, words):
    tags = convert_words_to_tags(words)
    if tags:
        queryset = filter_hangout_with_tags(tags)
    else:
        queryset = Hangout.objects.none()

    serializer = HangoutSerializer(queryset, many=True)
    return JsonResponse(serializer.data, status=201, safe=False)


@api_view()
def hangout_search_by_area_n_tags(request, area_name, words):
    area_related_tags = convert_area_name_to_tags(area_name)
    queryset = filter_hangout_with_area_related_tags(area_related_tags)

    tags = convert_words_to_tags(words)
    queryset = filter_hangout_with_tags(tags, queryset=queryset)

    serializer = HangoutSerializer(queryset, many=True)
    return JsonResponse(serializer.data, status=201, safe=False)


def convert_area_name_to_tags(area_name):
    try:
        area = Area.objects.get(name=area_name)
    except Area.DoesNotExist:
        return Tag.objects.none()
    else:
        return area.tag_set.all()


def convert_words_to_tags(words):
    words = words.split(',')
    return Tag.objects.filter(word__in=[*words])


def filter_hangout_with_area_related_tags(area_related_tags, *, queryset=None):
    queryset = Hangout.objects.all() if queryset is None else queryset

    queryset = queryset.filter(tags__in=list(area_related_tags))

    return queryset


def filter_hangout_with_tags(tags, *, queryset=None):
    queryset = Hangout.objects.all() if queryset is None else queryset

    for tag in tags:
        queryset = queryset.filter(tags__in=[tag])

    return queryset
