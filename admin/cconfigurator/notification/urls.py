from django.urls import path

from .views import NotificationView
from .views import NotificationDetailView

urlpatterns = [
    path('', NotificationView.as_view()),
    path('<int:pk>/', NotificationDetailView.as_view()),
]
