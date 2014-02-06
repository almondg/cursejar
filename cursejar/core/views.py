from django.shortcuts import render
from django.core.urlresolvers import reverse
from models import Challenge, Person, Word, Jar, FacebookPerson
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView


# Create your views here.


def index(request):
        return render(request, 'core/index.html', )


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
        result = reverse(viewname='challenge-details', current_app='core', args=[3])
        return result