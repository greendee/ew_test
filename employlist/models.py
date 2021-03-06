from __future__ import unicode_literals

from django.db import models
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
from django.core.urlresolvers import reverse

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

    first_letter = models.CharField(max_length=1, editable=False, \
                        db_index=True)

    def get_full_name(self):
        if self.patronymic:
            return '%s %s %s' % \
                (self.last_name, self.first_name, self.patronymic)
        else:
            return '%s %s' % (self.last_name, self.first_name)

    def get_name_with_position(self):
        return '%s (%s at %s)' % \
            (self.get_full_name(), self.position, self.department)

    get_name_with_position.short_description = 'Name with position'

    def is_employed_now(self):
        return (self.dismiss_date is None or \
                 self.dismiss_date >= date.today())

    is_employed_now.boolean = True
    is_employed_now.short_description = 'Is employed now'

    def __unicode__(self):
        return self.get_name_with_position()

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.first_letter = self.last_name[0]
        super(Employee, self).save(*args, **kwargs)
