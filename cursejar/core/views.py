import time, datetime
import requests
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.edit import CreateView
from core.forms import ChallengeForm, ChallengeFormSet
from django.http import HttpResponseRedirect
from  django.conf import settings
from models import Challenge, Person, PayPalUser, Jar


def index(request):
    return render_to_response("main/index.html",
                              RequestContext(request))


class ChallengeView(DetailView):
    model = Challenge
    template_name = 'main/challenge.html'

    def get_context_data(self, **kwargs):
        context = super(ChallengeView, self).get_context_data(**kwargs)
        object = context['object']

        context['is_time_up'] = datetime.datetime.now() > object.end_date
        context['sum_of_debt'] = Jar.objects.get(challenge=object).current_sum
        context['winner_user'] = Person.objects.get(name='yotam')

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
    fields = ['name', 'end_date', 'participant']

    def form_valid(self, challenge):
        challenge.save()
        return super(CreateChallenge, self).form_valid(challenge)
    
    def get_success_url(self):
        result = reverse(viewname='challenge-details', current_app='core', kwargs={'pk': self.object.pk})
        return result



def paypal_agreement(request):
    if request.user.is_authenticated():
        url = "https://svcs.sandbox.paypal.com/AdaptivePayments/Preapproval"
        cancel_absolute_uri = request.build_absolute_uri(reverse('index'))
        return_absolute_uri = request.build_absolute_uri(reverse('index'))
        headers = {
            "X-PAYPAL-SECURITY-USERID": "orkun.saitoglu_api1.paypal.com",
            "X-PAYPAL-SECURITY-PASSWORD": "BRCQECZAWSHZGCRM",
            "X-PAYPAL-SECURITY-SIGNATURE": "AiH2hRv9R8oBsbyGKEgJr0XuNWxrAH353ZcFTx91-TwvlBXvpQLns38A",
            "X-PAYPAL-REQUEST-DATA-FORMAT": "NV",
            "X-PAYPAL-RESPONSE-DATA-FORMAT": "NV",
            "X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T"
        }

        payload = {
            "cancelUrl": cancel_absolute_uri,
            "currencyCode": 'USD',
            "maxAmountPerPayment": '10.00',
            "maxNumberOfPayments": '2000',
            "maxTotalAmountOfAllPayments": '2000.00',
            "pinType": 'NOT_REQUIRED',
            "requestEnvelope": 'errorLanguage=en_US',
            "returnUrl": return_absolute_uri,
            "startingDate": time.strftime("20%y-%m-%dT00:00:00.000Z")
        }

        r = requests.post(url, data=payload, headers=headers)
        print r.text
        respDict = dict()
        for pair in r.text.split('&'):
            pairArr = pair.split('=')
            respDict[pairArr[0]] = pairArr[1]

        retUrl = "NO URL"

        if respDict['responseEnvelope.ack'] == "Success":
            retUrl = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-preapproval&preapprovalkey=' + respDict[
                'preapprovalKey']
            related_user = Person.objects.get(pk=request.user.profile.pk)
            paypal_user, created = PayPalUser.objects.get_or_create(person=related_user)
            paypal_user.pre_approval_key = respDict['preapprovalKey']
            paypal_user.save()

        else:
            retUrl = cancel_absolute_uri
        print retUrl

        # response = HttpResponse()

        return HttpResponseRedirect(retUrl)
    else:
        return HttpResponseRedirect(reverse('index'))


def paypal_charge_user(request):
    if request.user.is_authenticated():
        challenge_pk = request.POST['challenge']
        winner_pk = request.POST['winner-user']
        related_challenge = Challenge.objects.get(pk=challenge_pk)
        winner_user = Person.objects.get(pk=winner_pk)
        paying_user = Person.objects.get(pk=request.user.profile.pk)
        paying_paypal_user = PayPalUser.objects.get(person=paying_user)
        paid_amount_total = Jar.objects.get(challenge=related_challenge).current_sum
        #TODO: change back to calculate number_of_paying_participants

        number_of_paying_participants = related_challenge.participant.count()
        if number_of_paying_participants > 0:
            paid_amount_per_user = paid_amount_total/number_of_paying_participants
        else:
            paid_amount_per_user = paid_amount_total
        return_absolute_uri = request.build_absolute_uri(reverse('index'))
        cancel_absolute_uri = request.build_absolute_uri(reverse('challenge-details', kwargs={'pk': challenge_pk}))


        url3 = "https://svcs.sandbox.paypal.com/AdaptivePayments/PreapprovalDetails"

        headers3 = {
            "X-PAYPAL-SECURITY-USERID": "orkun.saitoglu_api1.paypal.com",
            "X-PAYPAL-SECURITY-PASSWORD": "BRCQECZAWSHZGCRM",
            "X-PAYPAL-SECURITY-SIGNATURE": "AiH2hRv9R8oBsbyGKEgJr0XuNWxrAH353ZcFTx91-TwvlBXvpQLns38A",
            "X-PAYPAL-REQUEST-DATA-FORMAT": "NV",
            "X-PAYPAL-RESPONSE-DATA-FORMAT": "NV",
            "X-PAYPAL-APPLICATION-ID": "APP-80W284485P519543T"
        }


        payload3 = {
            'actionType': 'PAY', #The action taken in the Pay request (that is, the PAY action)
            'currencyCode': 'USD', #The currency, e.g. US dollars
            'feesPayer': 'EACHRECEIVER',
            'memo': 'Example',
            'preapprovalKey': paying_paypal_user.pre_approval_key, #The preapproval key received in a Preapproval API response
            'receiverList.receiver(0).amount': paid_amount_per_user, #The payment amount
            'receiverList.receiver(0).email': winner_user.email,
            'senderEmail': paying_user.email,
            'returnUrl': return_absolute_uri, #For use if the customer proceeds with payment
            'cancelUrl': cancel_absolute_uri, #For use if the customer decides not to proceed with payment
            'requestEnvelope.errorLanguage': 'en_US'
        }

        if paid_amount_per_user > 0:
            r3 = requests.post(url3, data=payload3, headers=headers3)

            respDict3 = dict()

            for pair in r3.text.split('&'):
                pairArr = pair.split('=')
                respDict3[pairArr[0].upper()] = pairArr[1]

            if respDict3['RESPONSEENVELOPE.ACK'] == 'Success':
                print 'success!'
            else:
                print 'fail.. :('

            return HttpResponseRedirect(reverse('index'))
        else:
            print 'Nothing to pay on.'
            return HttpResponseRedirect(reverse('challenge-details', kwargs={'pk': challenge_pk}))


# def get_posts_from_facebook():
#     related_challenge = Challenge.objects.get(pk=pk)
#     list_of_participants =
#     graph = facebook.GraphAPI()
#     graph.access_token = facebook.get_app_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
#     graph.get_connections()