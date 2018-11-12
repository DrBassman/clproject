from django.contrib import admin
from .models import ContactAttribute, ContactLens, ContactRebate

# Register your models here.
class CAInline(admin.TabularInline):
    model = ContactAttribute.clenses.through
    extra = 0

class CRInline(admin.TabularInline):
    model = ContactRebate.lenses.through
    extra = 0

class ContactLensAdmin(admin.ModelAdmin):
    inlines = [CRInline, CAInline]

admin.site.register(ContactLens, ContactLensAdmin)
admin.site.register(ContactAttribute)
admin.site.register(ContactRebate)
