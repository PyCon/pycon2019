from django.conf.urls.defaults import patterns, url, include, handler404, handler500

urlpatterns = patterns("review.views",
    url(r"^list/$", "review_list", name="review_list"),
    url(r"^list/(?P<username>[\w]+)/$", "review_list", name="review_list_user"),
    url(r"^admin/$", "review_admin", name="review_admin"),
    url(r"^stats/$", "review_stats", name="review_stats"),
    url(r"^(?P<pk>\d+)/$", "review_detail", name="review_detail"),
    url(r"^assignments/$", "review_assignments", name="review_assignments"),
    url(r"^assignment/(?P<pk>\d+)/opt-out/$", "review_assignment_opt_out",
        name="review_assignment_opt_out"),
)
