from django.db import models
from django.contrib.auth.models import User
from labgeeksrpg.chronos.models import Location
from datetime import date

class TimePeriod(models.Model):
    """ Defines possible periods of time when a person could choose to work or choose not to work.
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(default=date.today())
    
    def __unicode__(self):
        return self.name

class WorkShift(models.Model):
    """ These are shifts that people are expected to work for. 
    """
    person = models.ForeignKey(User, null=True, blank=True)
    scheduled_in = models.DateTimeField()
    scheduled_out = models.DateTimeField()
    location = models.ForeignKey(Location)

    def __unicode__(self):
        if self.person:
            person_string = self.person
        else:
            person_string = "Open Shift"

        return "%s: [%s] %s-%s @%s" % (person_string,self.scheduled_in.date(),self.scheduled_in.time(),self.scheduled_out.time(), self.location)

class DefaultShift(models.Model):
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    person = models.ForeignKey(User, null=True, blank=True)
    day = models.CharField(max_length=256, choices=DAY_CHOICES)
    in_time = models.TimeField()
    out_time = models.TimeField()
    location = models.ForeignKey(Location)
    timeperiod = models.ForeignKey(TimePeriod, default=TimePeriod.objects.get(id=1), null=True, blank=True)

    def __unicode__(self):
        if self.person:
            person_string = self.person
        else:
            person_string = "Open Shift"

        return "%s: [%s] %s-%s @%s" % (person_string,self.day,self.in_time,self.out_time, self.location)

class ClosedHour(models.Model):
    DAY_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    day = models.CharField(max_length=256, choices=DAY_CHOICES)
    in_time = models.TimeField()
    out_time = models.TimeField()
    location = models.ForeignKey(Location)
    timeperiod = models.ForeignKey(TimePeriod)

    def __unicode__(self):
        return "[%s] %s-%s @%s" % (self.day,self.in_time,self.out_time, self.location)

