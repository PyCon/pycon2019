from django.conf.urls.defaults import patterns, url, include, handler404, handler500


urlpatterns = patterns("review.views",
    url(r"^list/$", "review_list", name="review_list"),
    url(r"^list/(?P<username>[\w]+)/$", "review_list", name="review_list_user"),
    url(r"^admin/$", "review_admin", name="review_admin"),
    url(r"^stats/$", "review_stats", name="review_stats"),
    url(r"^stats/(?P<key>[\w]+)/$", "review_stats", name="review_stats_key"),
    url(r"^(?P<pk>\d+)/$", "review_detail", name="review_detail"),
)
