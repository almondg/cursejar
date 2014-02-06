from django.shortcuts import render
from models import Challenge, Person, Word, Jar, FacebookPerson
from django.views.generic.detail import DetailView

# Create your views here.


def index(request):
        return render(request, 'core/index.html', )


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