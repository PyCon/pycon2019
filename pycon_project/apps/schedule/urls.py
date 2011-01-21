from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("schedule.views",
    # url(r"^$", "schedule_list", name="schedule_list"),
    # url(r"^sessions/(\d+)/", "schedule_session", name="schedule_session"),
    
    url(r"^$", direct_to_template, {"template": "schedule/index.html"}, name="schedule_index"),
    url(r"^lists/talks/", "schedule_list_talks", name="schedule_list_talks"),
    url(r"^lists/tutorials/", "schedule_list_tutorials", name="schedule_list_tutorials"),
    url(r"^tutorials/", "schedule_tutorials", name="schedule_tutorials"),
    url(r"^sessions/(\d+)/", "schedule_session", name="schedule_session"),
)