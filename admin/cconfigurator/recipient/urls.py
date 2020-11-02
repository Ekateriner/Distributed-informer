from django.urls import path

from .views import RecipientView, RecipientDetailView, ExceptRuleView, FilterRuleView

urlpatterns = [
    path('', RecipientView.as_view()),
    path('<int:pk>/', RecipientDetailView.as_view()),
    path('exceptrules/', ExceptRuleView.as_view()),
    path('filterrules/', FilterRuleView.as_view()),
]
