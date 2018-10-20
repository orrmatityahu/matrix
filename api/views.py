import threading

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Article, Scan
from api.serializers import ArticleSerializer, ScanSerializer
from utils.scan import scan


class ListArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows articles to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('text', 'title')

    @action(methods=['post'], detail=False, url_path='search', url_name='search')
    def search(self, request):
        query = request.data.get('query')

        if not query:
            return Response('query was not satisfied', status=status.HTTP_400_BAD_REQUEST)

        articles = Article.objects.filter(text__icontains=query)

        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data)


class ScanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scans to be viewed.
    """
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    def create(self, request, *args, **kwargs):
        scan_obj = Scan.objects.create()
        thread = threading.Thread(target=scan, kwargs={'scan_obj': scan_obj})
        thread.start()
        return Response({"message": "Scan Started", "Scan_id": scan_obj.id}, status=status.HTTP_200_OK)


