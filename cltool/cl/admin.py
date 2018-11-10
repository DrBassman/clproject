from django.contrib import admin
from .models import ContactAttribute, ContactLens

# Register your models here.
class CAInline(admin.TabularInline):
    model = ContactAttribute.clenses.through
    extra = 0

class ContactLensAdmin(admin.ModelAdmin):
    inlines = [CAInline]

admin.site.register(ContactLens, ContactLensAdmin)
admin.site.register(ContactAttribute)
