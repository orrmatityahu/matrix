
from rest_framework import serializers
from api.models import Article, Scan


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('url', 'title', 'text')

    def create(self, validated_data):
        return Article.objects.create(**validated_data)


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ('creation_date', 'status', 'status_message')

    def create(self, validated_data):
        return Scan.objects.create(**validated_data)