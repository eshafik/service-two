import time

from django.conf import settings
from django.core.cache import cache
import redis
from opentelemetry import trace
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from apps.twitter.models import FeedPost
from apps.twitter.serializer import FeedPostSerializer


class FeedDataListAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FeedPostSerializer
    tracer = trace.get_tracer(__name__)

    def get_queryset(self):
        with self.tracer.start_as_current_span('postgres_db_query') as span:
            if self.request.query_params.get('type') == 'delay':
                time.sleep(1)
            queryset = FeedPost.objects.all()
            span.set_attribute('sql queries', print(queryset.query))
            return queryset

    def list(self, request, *args, **kwargs):
        if request.query_params.get('type') == 'error':
            request.data['name']
        limit = self.request.query_params.get('limit', 10)
        page = self.request.query_params.get('page', 1)
        data = cache.get(f'feed_post:{page}:{limit}')
        if not data:
            resp = super().list(request, *args, **kwargs)
            print("data", resp.data, type(dict))
            cache.set(f'feed_post:{page}:{limit}', resp.data, timeout=10)
            return resp
        return Response(data=data)

    # der list
    # def get(self, request):
    #     tracer = trace.get_tracer(__name__)
    #     feed_post = cache.get("feed_post")
    #     if not feed_post:
    #         with tracer.start_as_current_span('db_query'):
    #             queryset = FeedPost.objects.all()
    #             serializer = FeedPostSerializer(queryset, many=True)
    #             feed_post = serializer.data
    #             cache.set("feed_post", feed_post)
    #     return Response(data=feed_post)