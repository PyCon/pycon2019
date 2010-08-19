from django.conf.urls.defaults import patterns, url, include, handler404, handler500

urlpatterns = patterns("schedule.views",
    url(r"^$", "schedule_list", name="schedule_list"),
    url(r"^sessions/(\d+)/", "schedule_session", name="schedule_session"),
)
