from django.urls import path
from django.views.decorators.cache import cache_page

from constant import Constant
from .views import SummarizeContentAPIView, AnalyzeContentAPIView, ContentListCreateAPIView, \
    ContentRetrieveUpdateDeleteAPIView, CategoryListAPIView

urlpatterns = [
    path(
        'categories/',
        cache_page(Constant.CACHE_TIMEOUT_1_WEEK, key_prefix='Category')
        (CategoryListAPIView.as_view()),
        name='categories',
    ),
    path('contents/', ContentListCreateAPIView.as_view(), name='content-list'),
    path('contents/<int:id>', ContentRetrieveUpdateDeleteAPIView.as_view(), name='content-update'),
    path('summarize/', SummarizeContentAPIView.as_view(), name='summarize-content'),
    path('analyze/', AnalyzeContentAPIView.as_view(), name='summarize-content'),
]
