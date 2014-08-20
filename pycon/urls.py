from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from . import views


urlpatterns = patterns(
    '',
    url('program_export/', views.program_export, name='program_export'),

    # Venue pages.
    url(r"^venue/$",
        TemplateView.as_view(template_name="venue/detail.html"),
        name="venue_detail"),
    url(r"^venue/bars/$",
        TemplateView.as_view(template_name="venue/bars.html"),
        name="bars"),
    url(r"^venue/cellphone/$",
        TemplateView.as_view(template_name="venue/cellphone.html"),
        name="cellphone"),
    url(r"^venue/directions/$",
        TemplateView.as_view(template_name="venue/directions.html"),
        name="directions"),
    url(r"^venue/explore/$",
        TemplateView.as_view(template_name="venue/explore.html"),
        name="explore"),
    url(r"^venue/getting-around/$",
        TemplateView.as_view(template_name="venue/getting_around.html"),
        name="getting_around"),
    url(r"^venue/hotels/$",
        TemplateView.as_view(template_name="venue/hotels.html"),
        name="hotels"),
    url(r"^venue/restaurants/$",
        TemplateView.as_view(template_name="venue/restaurants.html"),
        name="restaurants"),
    url(r"^venue/share-room/$",
        TemplateView.as_view(template_name="venue/share_room.html"),
        name="share_room"),
    url(r"^venue/shopping/$",
        TemplateView.as_view(template_name="venue/shopping.html"),
        name="shopping"),
    url(r"^venue/traveling/$",
        TemplateView.as_view(template_name="venue/traveling.html"),
        name="traveling"),
    url(r"^venue/weather/$",
        TemplateView.as_view(template_name="venue/weather.html"),
        name="weather"),
)
