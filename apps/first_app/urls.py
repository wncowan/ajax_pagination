from django.conf.urls import url
from . import views
from views import ChangePage, SearchName, StartDate

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new$', views.new),
    url(r'^create$', views.create),
    url(r'^changePage$', ChangePage.as_view(), name = "changePage"),
	url(r'^searchName$', SearchName.as_view(), name = "searchName"),
	url(r'^startDate$', StartDate.as_view(), name = "startDate")
]