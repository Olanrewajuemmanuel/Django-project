from .models import Article
from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    """
    Class to convert(serialize) DB syntax to JSON or other formats
    for an API
    """
    author = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=254)
    date = serializers.DateTimeField()

    #methods
    def create(self, validated_data):
        return Article.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.email = validated_data.get('email', instance.email)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'author',
            'email'
        ]

