from django.db import models

import datetime
# Create your models here.
class ContactLens(models.Model):
    clens = models.CharField(max_length=128)
    num_year_supply = models.IntegerField()
    cost_per_package = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return self.clens
    def has_rebate(self):
        cur_dt = datetime.date.today()
        rebates = self.contactrebate_set.exclude(to_dt__lt=cur_dt).exclude(from_dt__gt=cur_dt)
        if len(rebates):
            return "rebate"
        else:
            return ""
    class Meta:
        ordering = ["clens"]
        verbose_name_plural = "Contact lenses"


class ContactAttribute(models.Model):
    attribute = models.CharField(max_length=64)
    clenses = models.ManyToManyField(ContactLens)
    def __str__(self):
        return self.attribute
    class Meta:
        ordering = ["attribute"]

class ContactRebate(models.Model):
    desc = models.CharField(max_length=64)
    from_dt = models.DateField()
    to_dt = models.DateField()
    lenses = models.ManyToManyField(ContactLens)
    exclusive = models.BooleanField(default=True)
    amt = models.DecimalField(max_digits=7, decimal_places=2)
    half_amt = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    def __str__(self):
        return self.desc + ': ' + str(self.amt)
    class Meta:
        ordering = ["-to_dt"]

class ConfigDefaults(models.Model):
    def_cl_service_amt = models.DecimalField(max_digits=7, decimal_places=2)
    def_exam_amt = models.DecimalField(max_digits=7, decimal_places=2)
    def_benefit_amt = models.DecimalField(max_digits=7, decimal_places=2)
    class Meta:
        verbose_name_plural="Defaults (only 1 record)"
