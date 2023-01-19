from django.urls import path
from .views import FestivalListView, FestivalDetailView

urlpatterns = [
    path('', FestivalListView.as_view()),
    path('<int:pk>/', FestivalDetailView.as_view())
]
