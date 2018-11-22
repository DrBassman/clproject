from django import forms

import datetime

from .fields import HTML5DateInput

class FooForm(forms.Form):
    sale_date = forms.DateField(widget=HTML5DateInput, initial=datetime.date.today())
