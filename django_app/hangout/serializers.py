from rest_framework import serializers

from hangout.models import Hangout, Tag, Area


class TagSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = Tag


class HangoutSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Hangout
        fields = ('slug', 'title', 'description', 'address', 'latitude', 'longitude', 'tags')


class AreaSerializer(serializers.ModelSerializer):
    tag_set = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('name', 'address', 'tag_set')
