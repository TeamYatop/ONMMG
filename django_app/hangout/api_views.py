from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from hangout.models import Hangout, Tag, Area
from hangout.serializers import HangoutSerializer, AreaSerializer, TagSerializer


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
def hangout_search(request):
    area_name = request.query_params.get('area', None)
    words = request.query_params.get('tags', None)

    if (area_name is None) and (words is None):
        return HttpResponse(status=404)

    queryset = Hangout.objects.all()

    if area_name:
        area_related_tags = convert_area_name_to_tags(area_name)
        queryset = filter_hangout_with_area_related_tags(area_related_tags, queryset=queryset)

    if words:
        tags = convert_words_to_tags(words)
        queryset = filter_hangout_with_tags(tags, queryset=queryset)

    serializer = HangoutSerializer(queryset, many=True)
    return JsonResponse(serializer.data, status=201, safe=False)


@api_view()
def hangout_tags(request):
    try:
        tags = Tag.objects.all()
    except Tag.DoesNotExist:
        return HttpResponse(status=404)
    else:
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, status=201, safe=False)


@api_view()
def hangout_areas(request):
    try:
        areas = Area.objects.all()
    except Area.DoesNotExist:
        return HttpResponse(status=404)
    else:
        serializer = AreaSerializer(areas, many=True)
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

    if area_related_tags:
        queryset = queryset.filter(tags__in=list(area_related_tags))
    else:
        queryset = Hangout.objects.none()

    return queryset


def filter_hangout_with_tags(tags, *, queryset=None):
    queryset = Hangout.objects.all() if queryset is None else queryset

    if tags:
        for tag in tags:
            queryset = queryset.filter(tags__in=[tag])
    else:
        queryset = Hangout.objects.none()

    return queryset
