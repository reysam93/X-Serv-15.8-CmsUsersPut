from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Page


def processCmsRequest(request, resource):
    if request.user.is_authenticated():
        loged = "<br><br>Logged in as " + request.user.username +\
                ". <a href='/admin/logout/'>Logout</a><br>"
    else:
        loged = "<br><br>Not logged. <a href='/admin/login/'>Login</a><br>"
    if request.method == 'GET':
        try:
            page = Page.objects.get(name=resource)
            return HttpResponse(page.page + loged)
        except Page.DoesNotExist:
            return HttpResponseNotFound("Page not found" + loged)
    elif request.method == 'PUT':
        if request.user.is_authenticated():
            try:
                newPage = Page.objects.get(name=resource)
                newPage.page = request.body
            except Page.DoesNotExist:
                newPage = Page(name = resource, page = request.body)
            newPage.save()
            return HttpResponse("Added to the list")
        else:
            return HttpResponse("Couldn't add to the list" + loged)
    else:
        return HttpResponse(status=403)
