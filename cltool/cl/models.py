from django.db import models

# Create your models here.
class ContactLens(models.Model):
    clens = models.CharField(max_length=128)
    num_year_supply = models.IntegerField()
    cost_per_package = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return self.clens

class ContactAttribute(models.Model):
    attribute = models.CharField(max_length=64)
    clenses = models.ManyToManyField(ContactLens)
    def __str__(self):
        return self.attribute

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
