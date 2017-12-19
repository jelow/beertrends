from django.conf.urls import url
from . import views

app_name = 'userprofile'
urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'^addBeer/(?P<beer_id>\w+)/$', views.add_beer_to_wishlist, name='add_beer_to_wishlist'),
    url(r'^removeBeer/(?P<beer_id>\w+)/$', views.remove_beer_from_wishlist, name='remove_beer_from_wishlist'),
    url(r'^addBrewery/(?P<brewery_id>\w+)/$', views.add_brewery_to_watchlist, name='add_brewery_to_watchlist'),
    url(r'^removeBrewery/(?P<brewery_id>\w+)/$', views.remove_brewery_from_watchlist, name='remove_brewery_from_watchlist'),
    url(r'^dismiss/(?P<notification_id>\w+)/$', views.dismiss_notification, name='dismiss_notification'),
]
