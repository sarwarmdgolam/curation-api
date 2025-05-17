from rest_framework import serializers
from .models import Content, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ('summary', 'sentiment')


class SummarizeSerializer(serializers.Serializer):
    content = serializers.CharField()