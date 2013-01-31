import hashlib

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Session, SessionRole


def session_list(request):
    
    sessions = Session.objects.all()
    
    return render(request, "schedule/session_list.html", {
        "sessions": sessions,
    })


@login_required
def session_staff_email(request):
    
    if not request.user.is_staff:
        return redirect("schedule_session_list")
    
    data = "\n".join(user.email for user in User.objects.filter(sessionrole__isnull=False).distinct())
    
    return HttpResponse(data, content_type="text/plain;charset=UTF-8")


def session_detail(request, session_id):
    
    session = get_object_or_404(Session, id=session_id)
    
    chair = None
    chair_denied = False
    chairs = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_CHAIR).exclude(status=False)
    if chairs:
        chair = chairs[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(session=session, user=request.user, role=SessionRole.SESSION_ROLE_CHAIR, status=False):
                chair_denied = True
    
    runner = None
    runner_denied = False
    runners = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_RUNNER).exclude(status=False)
    if runners:
        runner = runners[0].user
    else:
        if request.user.is_authenticated():
            # did the current user previously try to apply and got rejected?
            if SessionRole.objects.filter(session=session, user=request.user, role=SessionRole.SESSION_ROLE_RUNNER, status=False):
                runner_denied = True
    
    if request.method == "POST" and request.user.is_authenticated():
        if not hasattr(request.user, "profile") or not request.user.profile.is_complete:
            response = redirect("profile_edit")
            response["Location"] += "?next=%s" % request.path
            return response
        
        role = request.POST.get("role")
        if role == "chair":
            if chair == None and not chair_denied:
                SessionRole(session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user).save()
        elif role == "runner":
            if runner == None and not runner_denied:
                SessionRole(session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user).save()
        elif role == "un-chair":
            if chair == request.user:
                session_role = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_CHAIR, user=request.user)
                if session_role:
                    session_role[0].delete()
        elif role == "un-runner":
            if runner == request.user:
                session_role = SessionRole.objects.filter(session=session, role=SessionRole.SESSION_ROLE_RUNNER, user=request.user)
                if session_role:
                    session_role[0].delete()
        
        return redirect("schedule_session_detail", session_id)
    
    return render(request, "schedule/session_detail.html", {
        "session": session,
        "chair": chair,
        "chair_denied": chair_denied,
        "runner": runner,
        "runner_denied": runner_denied,
    })
