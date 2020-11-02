from django.urls import path

from .views import *

urlpatterns = [
    path('uplinkstats/', UplinkStatView.as_view()),
    path('borders/', BorderView.as_view()),
    path('sitelatencies/', SiteLatencyView.as_view()),
    path('sites/', SiteView.as_view()),
    path('nodes/', NodeView.as_view()),
    path('tagdict/', TagDict.as_view()),
    path('nodelatencies/', NodeLatencyView.as_view()),
    path('services/', ServiceView.as_view()),
    path('nodeips/', NodeIpView.as_view()),
]
