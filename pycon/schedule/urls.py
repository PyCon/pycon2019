from django.conf.urls.defaults import url, patterns


urlpatterns = patterns("pycon.schedule.views",
    url(r"^sessions/staff.txt$", "session_staff_email", name="schedule_session_staff_email"),
    url(r"^sessions/$", "session_list", name="schedule_session_list"),
    url(r"^session/(\d+)/$", "session_detail", name="schedule_session_detail"),
)
