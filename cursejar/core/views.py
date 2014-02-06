from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

import cgi
import urllib

from cursejar.settings import local
import models

from models import Challenge, Person


# Create your views here.


def index(request):

    return render_to_response("main/index.html",
                              RequestContext(request))


def login(request):
    error = None

    if request.user.is_authenticated():
        return HttpResponseRedirect('/yay/')

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': local.FACEBOOK_APP_ID,
                'redirect_uri': local.FACEBOOK_REDIRECT_URI,
                'client_secret': local.FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }

            url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            access_token = response['access_token'][0]
            expires = response['expires'][0]

            facebook_session = models.FacebookSession.objects.get_or_create(
                access_token=access_token,
            )[0]

            facebook_session.expires = expires
            facebook_session.save()

            user = auth.authenticate(token=access_token)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect('/yay/')
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    template_context = {'settings': local, 'error': error}
    return render_to_response('core/login.html', template_context, context_instance=RequestContext(request))

class ChallengeView(DetailView):
    model = Challenge
    template_name = 'core/challenge.html'


class PersonView(DetailView):
    model = Person
    template_name = 'core/person.html'
    #
    # def get_context_data(self, **kwargs):
    #     context = super(PersonView, self).get_context_data(**kwargs)
    #     pk = self.kwargs['pk']
    #     person = Person.objects.get(pk=pk)
    #     context['']
    #     return  context

