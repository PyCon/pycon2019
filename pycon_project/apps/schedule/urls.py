from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("schedule.views",
    # url(r"^$", "schedule_list", name="schedule_list"),
    # url(r"^presentations/(\d+)/", "schedule_presentation", name="schedule_presentation"),
    
    url(r"^$", direct_to_template, {"template": "schedule/index.html"}, name="schedule_index"),
    
    url(r"^lists/talks/", "schedule_list_talks", name="schedule_list_talks"),
    url(r"^lists/tutorials/", "schedule_list_tutorials", name="schedule_list_tutorials"),
    url(r"^lists/posters/", "schedule_list_posters", name="schedule_list_posters"),
    
    url(r"^tutorials/", "schedule_tutorials", name="schedule_tutorials"),
    url(r"^presentations/(\d+)/", "schedule_presentation", name="schedule_presentation"),
    
    url(r"^tracks/$", "track_list", name="schedule_track_list"),
    url(r"^sessions/$", "session_list", name="schedule_session_list"),
    url(r"^track/(\d+)/$", "track_detail", name="schedule_track_detail"),
    url(r"^session/(\d+)/$", "session_detail", name="schedule_session_detail"),
)