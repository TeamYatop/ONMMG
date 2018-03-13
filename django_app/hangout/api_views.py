from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

from hangout.models import Hangout, Tag
from hangout.serializers import HangoutSerializer


def hangout_list(request):
    if request.method == 'GET':
        hangouts = Hangout.objects.all()
        serializer = HangoutSerializer(hangouts, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HangoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def hangout_detail(request, slug):
    try:
        hangout = Hangout.objects.get(slug=slug)
    except Hangout.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HangoutSerializer(hangout)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HangoutSerializer(hangout, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        hangout.delete()
        return HttpResponse(status=204)


def hangout_search_by_tags(request, words):
    words = words.split(',')
    tags = list()
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
    else:
        queryset = Hangout.objects.none()

    serializer = HangoutSerializer(queryset, many=True)
    return JsonResponse(serializer.data, status=201, safe=False)


def hangout_search_by_area_n_tags(request, area, words):
    pass
