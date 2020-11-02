from django.urls import path

from .views import TemplateView, TemplateDetailView

urlpatterns = [
    path('', TemplateView.as_view()),
    path('<int:pk>/', TemplateDetailView.as_view()),
]
