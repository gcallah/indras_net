# from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .models import Model
from .models import ModelParam

from django import forms

from indra.api import get_agent

#RUN = 'run'
#STEP = 'step'
#SHOW = 'show'
MODEL = 'model'
HEADER = 'header'
DEFAULT_HIGHVAL = 100000
DEFAULT_LOWVAL = 0

def get_hdr():
    site_hdr = "Indra's Net"
#    site_list = Site.objects.all()
#    for site in site_list:
#        site_hdr = site.header
#        break   # since we only expect a single site record!
    return site_hdr

def dump_dict(d, vmachine):
    for key, val in d.items():
        add_debug(str(key) + ": " + str(val), vmachine)

def main_page(request):
    site_hdr = get_hdr()

    models = Model.objects.order_by('mtype')
    template_data = {'models': models, HEADER: site_hdr}
    return render(request, 'main.html', template_data)

def ab_models(request):
    site_hdr = get_hdr()

    models = Model.objects.order_by('mtype')
    template_data = {'models': models, HEADER: site_hdr}
    return render(request, 'abmodels.html', template_data)

def parameters(request):
    class ParamForm(forms.Form):
        def __init__(self, *args, **kwargs):
            questions = kwargs.pop('questions')
            super(ParamForm, self).__init__(*args, **kwargs)
            for q in questions:
                default = ""
                lowval, hival = DEFAULT_LOWVAL, DEFAULT_HIGHVAL
                if q.default_val:
                    default = q.default_val
                if q.lowval:
                    lowval = q.lowval
                if q.hival:
                    hival = q.hival
                if q.atype == "STR":
                    self.fields[q.question] = forms.CharField(label=q.question, 
                               initial=default, max_length=20)
                if q.atype == "INT":
                    self.fields[q.question] = forms.IntegerField(label=q.question, 
                               initial=default, min_value=lowval, 
                               max_value=hival)
                if q.atype == "DBL":
                    self.fields[q.question] = forms.FloatField(label=q.question, 
                               initial=default, min_value=lowval, 
                               max_value=hival)
                if q.atype == "BOOL":
                    self.fields[q.question] = forms.BooleanField(label=q.question, 
                               required=False)
    
    site_hdr = get_hdr()
    model_name = request.GET[MODEL]
    model = Model.objects.get(name=model_name)
    form = ParamForm(questions=model.params.all())
    
    template_data = {'form': form, HEADER: site_hdr}
    return render(request, 'parameters.html', template_data)

def run(request):
    site_hdr = get_hdr()
    model_name = request.POST[MODEL]
    model = Model.objects.get(name=model_name)
    questions = model.params.all()
    answers = []
    for q in questions:
        answers.append(request.POST[q.question])
    template_data = {'answers': answers, HEADER: site_hdr}
    return render(request, 'run.html', template_data)

#def main_page(request):
#    site_hdr = get_hdr()
#    response = ""
#    json = ""
#    if request.method == 'GET':
#        form = MainForm()
#    else:
#        form = MainForm(request.POST)
#    if RUN in request.POST:
#        response = "Run "
#    if STEP in request.POST:
#        response += request.POST[STEP] + " steps!"
#    if SHOW in request.POST:
#        json = get_agent(0)
#    return render(request, 'main.html',
#                  {'form': form,
#                   'response': response, 
#                   'json': json, 
#                   HEADER: site_hdr
#                  })

def help(request):
    site_hdr = get_hdr()
    return render(request, 'help.html', {HEADER: site_hdr})

def feedback(request):
    site_hdr = get_hdr()
    email_list = AdminEmail.objects.all()
    comma_del_emails = ""
    for email in email_list:
        comma_del_emails = comma_del_emails + email.email_addr + ","
    comma_del_emails = comma_del_emails[:-1]
    return render(request, 'feedback.html', {'emails': comma_del_emails,
        HEADER: site_hdr})
