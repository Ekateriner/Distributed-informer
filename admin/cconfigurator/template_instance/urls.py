from django.urls import path

from template_instance.views import TemplateInstanceView
from template_instance.views import TemplateInstanceDetailView

urlpatterns = [
    path('', TemplateInstanceView.as_view()),
    path('<int:pk>/', TemplateInstanceDetailView.as_view()),
]
