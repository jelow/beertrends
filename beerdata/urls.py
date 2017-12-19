from django.conf.urls import url
from . import views

app_name = 'webhooks'

urlpatterns = [
	url(r'update/beer$', views.handle_update_beer, name='handle_update_beer'),
	url(r'update/brewery$', views.handle_update_brewery, name='handle_update_brewery'),
	url(r'search_beers$', views.search_beers, name='search_beers'),
]
