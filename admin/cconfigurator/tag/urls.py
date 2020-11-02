from django.urls import path

from .views import TagView
from .views import TagDetailView

urlpatterns = [
    path('', TagView.as_view()),
    path('<int:pk>/', TagDetailView.as_view()),
]
