# -*- coding: utf-8 -*-
from django import forms
from django.core import serializers

import pandas as pd
# import crispy_forms to improve layouts
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
        Layout,
        Div,
        Submit,
        HTML,
        Button,
        Row,
        Field,
        Fieldset,
        )
from crispy_forms.bootstrap import FormActions, InlineRadios, Accordion, AccordionGroup, Tab, TabHolder

from .models import Portfolio

# Function based form declarations

def get_my_choices():
    '''
    Get list of currently saved portfolios here
    '''
    print("get_my_choices")
#    queryset = Portfolio.objects.all()
    
#    XMLSerializer = serializers.get_serializer("xml")
#    xml_serializer = XMLSerializer()
#    xml_serializer.serialize(queryset)
#    data = xml_serializer.getvalue()

#    JSONSerializer = serializers.get_serializer("json")
#    json_serializer = JSONSerializer()
#    json_serializer.serialize(queryset)
#    data = json_serializer.getvalue()

#    data = ['None', 'Anonymous',]

    data = Portfolio.objects.all()
#    print(len(data), type(data))
#    print(data)
    
    data_tuple = tuple((o.id, o.pname) for o in data)
    print(data_tuple)
#    data_list = list(Portfolio.objects.values_list('name', flat=True).distinct())
#    print(type(data_list))
#    print(data_list)

#    print(len(data_tuple), type(data_tuple))
#    print(data_tuple)
    
#    portfolio_list = list(data)
#    print(portfolios_list)
    return data_tuple


class PortfolioForm(forms.ModelForm):
    print("PortfolioForm")
    
#    pname = forms.TypedChoiceField(
#        label = "Portfolio",
##        choices=my_choices,
#    )
            
#    FormActions(
#        Submit('submit', 'Lorem plot', css_class="btn-primary"),
#    )
            
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-4'
#    helper.layout = Layout(
#        Fieldset('Are these months classified correctly?',
#             'name',
#        ),
#     )                       
        
    def __init__(self, *args, **kwargs):
        my_choices = (
                ('anonymous', 'anonymous'),
                ('platforms', 'platforms'),
                )
        # http://www.ilian.io/django-forms-choicefield-with-dynamic-values/
        super(PortfolioForm, self).__init__(*args, **kwargs)
#        self.fields['name'] = forms.ChoiceField(choices=my_choices) 
        self.fields['pname'] = forms.ChoiceField(choices=get_my_choices())
        
    class Meta:
        model = Portfolio
        fields = (
                'pname',
                )
        
# Class based form declarations
class SubmitCryptoasset(forms.Form):
    url = forms.URLField()