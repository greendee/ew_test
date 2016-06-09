from __future__ import unicode_literals

from django.db import models
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Department(models.Model):
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField()
    email      = models.EmailField(blank=True)
    phone      = PhoneNumberField(blank=True) # external lib is better at this

    employ_date  = models.DateField()
    dismiss_date = models.DateField(null=True, blank=True)
    department   = models.ForeignKey(Department, related_name='employees')
    position     = models.CharField(max_length=255)

    def get_full_name(self):
        if self.patronymic:
            return '%s %s %s' % \
                (self.first_name, self.patronymic, self.last_name)
        else:
            return '%s %s' % (self.first_name, self.last_name)

    def get_name_with_position(self):
        return '%s (%s at %s)' % \
            (self.get_full_name(), self.position, self.department)

    def is_employed_now(self):
        return (self.dismiss_date is None or self.dismiss_date < date.today())

    is_employed_now.boolean = True

    def __unicode__(self):
        return self.get_name_with_position()
