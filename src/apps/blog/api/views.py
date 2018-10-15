from rest_framework.generics import (
    GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny

from ..models import ArticleRate
from .serializers import ArticleRateSerializer


class ArticleRateDetailsAPIView(RetrieveAPIView, GenericAPIView):
    """Obtener datos de un ArticleRate concreto."""
    queryset = ArticleRate.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ArticleRateSerializer


class ArticleRatePositiveUpdateAPIView(RetrieveUpdateAPIView, GenericAPIView):
    """Incrementar en 1 un ArticleRate."""
    queryset = ArticleRate.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ArticleRateSerializer

    def put(self, request, *args, **kwargs):
        if ArticleRate.objects.add_positive_article(request, kwargs.get('pk')):
            return super().update(request, *args, **kwargs)
        return None
