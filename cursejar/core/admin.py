from django.contrib import admin
from models import Jar, Challenge, Person, ChargeEvent, Word, UserProfile, PayPalUser

# Register your models here.

admin.site.register(Jar)
admin.site.register(Challenge)
admin.site.register(Person)
admin.site.register(ChargeEvent)
admin.site.register(Word)
admin.site.register(UserProfile)
admin.site.register(PayPalUser)