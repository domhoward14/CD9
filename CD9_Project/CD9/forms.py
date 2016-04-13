from django import forms
from django.utils.safestring import mark_safe

SITES = 1
APPS = 2
CALLS = 3
TEXTS = 4
SOCIAL_MEDIA = 5
CHOICES=[('select1','Yes'),
         ('select2','No')]

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class SitesForm (forms.Form):
    active = forms.ChoiceField(label= "Enable Site Name Trigger Check" , choices=CHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))
    triggerWord = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    form_type = forms.IntegerField(initial=SITES, widget = forms.HiddenInput())

class AppsForm (forms.Form):
    active = forms.ChoiceField(label= "Enable App Name Trigger Check" , choices=CHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))
    triggerWord = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    form_type = forms.IntegerField(initial=APPS, widget = forms.HiddenInput())

class CallsForm (forms.Form):
    active = forms.ChoiceField(label= "Enable Phone Number Trigger Check" , choices=CHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))
    triggerWord = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    form_type = forms.IntegerField(initial=CALLS, widget = forms.HiddenInput())

class TextsForm (forms.Form):
    active = forms.ChoiceField(label= "Enable Text Trigger Check" , choices=CHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))
    triggerWord = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    form_type = forms.IntegerField(initial=TEXTS, widget = forms.HiddenInput())

class SocialMediaForm (forms.Form):
    active = forms.ChoiceField(label= "Enable Social Media Trigger Check" , choices=CHOICES, widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))
    triggerWord = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}))
    form_type = forms.IntegerField(initial=SOCIAL_MEDIA, widget = forms.HiddenInput())
