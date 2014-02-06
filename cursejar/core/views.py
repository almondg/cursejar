from django.shortcuts import render
from django.core.urlresolvers import reverse
from models import Challenge, Person, Word, Jar, FacebookPerson
from django.views.generic.detail import DetailView
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView, CreateView

import cgi
import urllib

from cursejar.settings import local
import models




# Create your views here.


def index(request):
    return render_to_response("main/index.html",
                              RequestContext(request))

class ChallengeView(DetailView):
    model = Challenge
    template_name = 'core/challenge.html'


class PersonView(DetailView):
    model = Person
    template_name = 'core/user_dashboard.html'


class CreateChallenge(CreateView):
    model = Challenge
    fields = ['name', 'end_date', 'participant']

    def form_valid(self, challenge):
        challenge.save()
        return super(CreateChallenge, self).form_valid(challenge)
    
    def get_success_url(self):
        result = reverse(viewname='challenge-details', current_app='core', kwargs={'pk': self.object.pk})
        return result