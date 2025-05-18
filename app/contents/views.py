from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import filters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
)

from .ai import summarize_with_groq, analyze_sentiment_with_groq, extract_topics_with_groq, recommend_related_with_groq
from .models import Content, Category
from .serializers import ContentSerializer, SummarizeSerializer, CategorySerializer
from .permissions import IsOwnerOrAdmin

from app.contents.tasks.background import process_content


class CategoryListAPIView(ListAPIView):
    """Handle listing categories."""

    model = Category
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.filter(is_active=True).order_by('name')


class ContentListCreateAPIView(ListCreateAPIView):
    """Handle creating and listing contents."""

    model = Content
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    queryset = Content.objects.select_related('author').all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'author': ['exact'],
        'created_at': ['date__range'],
        'category__name': ['contains'],
    }
    search_fields = [
        'title',
        'body',
        'summary',
        'sentiment',
    ]
    ordering_fields = [
        'id',
        'created_at',
        'updated_at',
    ]

    def create(self, request, *args, **kwargs):
        """Add content."""
        request.data._mutable = True
        request.data['author'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        process_content.apply_async(args=[serializer.data.get('id')])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContentRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    """Handle retrieve, update, delete of Content."""

    model = Content
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_field = 'id'


class SummarizeContentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SummarizeSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data['content']
            try:
                summary = summarize_with_groq(content)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"summary": summary}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyzeContentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content', '')
        other_articles = request.data.get('related_candidates', [])

        sentiment = analyze_sentiment_with_groq(content)
        topics = extract_topics_with_groq(content)
        related = recommend_related_with_groq(content, other_articles)

        return Response({
            "sentiment": sentiment,
            "topics": topics,
            "related_articles": related
        })
