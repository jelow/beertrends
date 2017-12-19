from django.conf.urls import url
from . import views

app_name = 'recommender'

urlpatterns = [
	url(r'^$', views.recommender, name='recommender'),
	url(r'recommend/$', views.make_recommendation, name='recommend'),
]
