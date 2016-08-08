from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    url(r'blacklist/$', views.MsisdnBlacklist.as_view()),
    url(r'msisdnBlacklistStatus/$', views.MsisdnBlacklistStatus.as_view()),
    url(r'msisdnCloseRelationship/$', views.MsisdnCloseRelationship.as_view()),
    url(r'msisdnFraudScore/$', views.MsisdnFraudScore.as_view()),
    url(r'msisdnGangDetection/$', views.MsisdnGangDetection.as_view()),
    url(r'msisdnFraudDetection/$', views.MsisdnFraudDetection.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
