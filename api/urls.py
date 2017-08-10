# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListAndCreateView, RetriveAndUpdateAndDestroyView
from rest_framework.documentation import include_docs_urls

urlpatterns = {
    url(r'^$', ListAndCreateView.as_view(), name="list_all_and_create"),
    url(r'^(?P<pk>[0-9]+)/$', RetriveAndUpdateAndDestroyView.as_view(), name="detail_update_destroy")
}

urlpatterns = format_suffix_patterns(urlpatterns)