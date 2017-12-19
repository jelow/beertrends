from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'beertrends'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^admin/', admin.site.urls),
    url(r'^recommender/', include('recommender.urls')),
    url(r'^webhooks/', include('beerdata.urls')),
    url(r'^beerdata/', include('beerdata.urls')),
    url(r'^trends/', include('trends.urls')),
    url(r'^profiles/', include('userprofile.urls')),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url('^', include('django.contrib.auth.urls'))
]
