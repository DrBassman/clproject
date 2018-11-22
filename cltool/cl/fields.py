from django import forms

class HTML5DateInput(forms.DateInput):
    input_type = 'date'
