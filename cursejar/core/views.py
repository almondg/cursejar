from allauth import models
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm, modelformset_factory

from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.edit import CreateView
from django.forms.formsets import formset_factory
from djangotoolbox.fields import ListField
from core.forms import ChallengeForm, ChallengeFormSet, StringListField

from models import Challenge, Person


def index(request):
    return render_to_response("main/index.html",
                              RequestContext(request))


class ChallengeView(DetailView):
    model = Challenge
    template_name = 'main/challenge.html'


class PersonView(DetailView):
    model = Person
    template_name = 'main/user_dashboard.html'


class AllChallenges(DetailView):
    model = Person
    template_name = 'main/all_challenges.html'


class AddChallengeView(CreateView):
    template_name = 'main/add_challenge.html'
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
    fields = ['name', 'end_date', 'participant']

    def form_valid(self, challenge):
        challenge.save()
        return super(CreateChallenge, self).form_valid(challenge)
    
    def get_success_url(self):
        result = reverse(viewname='challenge-details', current_app='core', kwargs={'pk': self.object.pk})
        return result


