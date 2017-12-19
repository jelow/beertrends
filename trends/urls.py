from django.conf.urls import url
from . import views

app_name = 'trends'

urlpatterns = [
	url(r'^$', views.trends, name='trends'),
]
