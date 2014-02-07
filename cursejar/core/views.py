
from django.core.urlresolvers import reverse
import datetime
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.edit import CreateView
import facebook
from django.conf import settings

from core.forms import ChallengeForm, ChallengeFormSet
from cursejar import settings
from cursejar.settings import local
from models import Challenge, Person, ChargeEvent


def index(request):
    return render_to_response("main/index.html",
                              RequestContext(request))


class ChallengeView(DetailView):
    model = Challenge
    template_name = 'main/challenge.html'

    def get_context_data(self, **kwargs):
        context = super(ChallengeView, self).get_context_data(**kwargs)
        graph = facebook.GraphAPI(access_token='CAACEdEose0cBAPRrfAj0O0MANogYvQmsSvh1tmFbeBddcRaOonp9dy5MOkW4S2kufOs7R7L6LIN78rKSZAyn5HFjoLySSZAQPhXPhjOjOiOkmvPuoYFFLsqzY8mUEcx4Dv6ZAnjj010tPHq4WNCyErHbEvkwHF3GCiYifXkCof3olSavPBcEKrqoM7CTeoZD')
        challenge = context['object']

        jar = challenge.jar.all()[0]
        words = [challenge.word1, challenge.word2, challenge.word3]
       # graph.access_token = facebook.get_app_access_token(local.FACEBOOK_APP_ID, local.FACEBOOK_SECRET_KEY)
        for participant in challenge.participant.all():
            # profile = participant.profile.all()[0]
           # posts = graph.get_connections(participant.profile.username, 'posts')['data']
            posts = graph.get_connections('yotammanor', 'posts')['data']
            for post in posts:
                for word in words:
                    if word in post['message']:
                        print 'found', word
                        charge_event = ChargeEvent.objects.create(jar=jar, crime=word, felon=participant)
                        charge_event.date_of_felony = datetime.datetime.now()
                        charge_event.save()
                        print 'saved'
        return context

class PersonView(DetailView):
    model = Person
    template_name = 'main/user_dashboard.html'


class AllChallenges(DetailView):
    model = Person
    template_name = 'main/all_challenges.html'


class AddChallengeView(CreateView):
    template_name = 'main/challenge_form.html'
    form_class = ChallengeForm

    def get_context_data(self, **kwargs):
        context = super(AddChallengeView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChallengeFormSet(self.request.POST)
        else:
            context['formset'] = ChallengeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())  # assuming your model has ``get_absolute_url`` defined.
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CreateChallenge(CreateView):
    model = Challenge
    fields = ['name', 'end_date', 'participant', 'word1', 'word2', 'word3']


    def form_valid(self, challenge):
        challenge.save()
        return super(CreateChallenge, self).form_valid(challenge)

    def get_success_url(self):
        result = reverse(viewname='challenge-details', current_app='core', kwargs={'pk': self.object.pk})
        return result


class FacebookView(DetailView):

    def get_posts_from_facebook(pk):
        related_challenge = Challenge.objects.get(pk=pk)
        list_of_participants = related_challenge.get('participant')
        word1 = related_challenge.get('word1')
        graph = facebook().GraphAPI()
        graph.access_token = facebook.get_app_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
        posts = graph.get_connections(id, 'posts')


