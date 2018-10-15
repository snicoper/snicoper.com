from rest_framework import serializers

from ..models import ArticleRate


class ArticleRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleRate
        fields = ('article', 'positives')
