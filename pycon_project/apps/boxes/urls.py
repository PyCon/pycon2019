from django.conf.urls.defaults import url, patterns


urlpatterns = patterns("boxes.views",
    url(r"^([-\w]+)/create/$", "box_create", name="box_create"),
    url(r"^(\d+)/edit/$", "box_edit", name="box_edit"),
)
