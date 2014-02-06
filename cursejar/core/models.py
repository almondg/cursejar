from django.db import models

# Create your models here.

DEFAULT_FINE_FOR_WORD = 1


class FacebookPerson(models.Model):
    pass


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return unicode(self.name)


class Challenge(models.Model):
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField()
    name = models.CharField(max_length=128)
    participant = models.ManyToManyField(Person, related_name='participants')

    def __unicode__(self):
        return unicode(self.name)


class Jar(models.Model):
    challenge = models.ForeignKey('Challenge')
    current_sum = models.FloatField(default=0)

    def __unicode__(self):
        return self.id


class ChargeEvent(models.Model):
    jar = models.ForeignKey('Jar')
    date_of_felony = models.DateTimeField(auto_now=True)
    felon = models.ForeignKey('Person')
    crime = models.ForeignKey('Word')
    evidence = models.URLField()

    def __unicode__(self):
        return unicode(self.felon) + \
               " " + unicode(self.crime) + \
               " " + unicode(self.date_of_felony)


class Word(models.Model):
    challenge = models.ForeignKey('Challenge')
    name = models.CharField(max_length=128, null=False)
    fine = models.IntegerField(default=DEFAULT_FINE_FOR_WORD)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = ('name', 'challenge')

