from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from .models import ContactAttribute, ContactLens, ContactRebate, ConfigDefaults

class ContactLensAdminForm(forms.ModelForm):
    class Meta:
        model = ContactLens
        fields = '__all__'
    attributes = forms.ModelMultipleChoiceField(
        queryset = ContactAttribute.objects.all(),
        required = False,
        widget = FilteredSelectMultiple(
            verbose_name = 'Contact Lens Attributes',
            is_stacked = False
        )
    )
    def __init__(self, *args, **kwargs):
        super(ContactLensAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['attributes'].initial = self.instance.contactattribute_set.all()
    def save(self, commit=True):
        attribute = super(ContactLensAdminForm, self).save(commit=False)
        attribute.save()
        attribute.contactattribute_set.set(self.cleaned_data['attributes'])
        self.save_m2m()
        return attribute

# Register your models here.
class CAInline(admin.TabularInline):
    model = ContactAttribute.clenses.through
    extra = 0

class CRInline(admin.TabularInline):
    model = ContactRebate.lenses.through
    extra = 0

class ContactLensAdmin(admin.ModelAdmin):
    form = ContactLensAdminForm

admin.site.register(ContactLens, ContactLensAdmin)
admin.site.register(ContactAttribute)
admin.site.register(ContactRebate)
admin.site.register(ConfigDefaults)
