########################################################################################
#  REFERENCES
#  Title: cal/forms.py
#  Author: Hui Wen
#  Date: 7/29/2018
#  URL: https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
#  Software License: <license software is released under>
########################################################################################

from django.forms import ModelForm, DateInput
from .models import Event, StudentClass
from django import forms

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ('title', 'description', 'start_time')

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class JoinForm(forms.Form):
    classes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=StudentClass.objects.all())