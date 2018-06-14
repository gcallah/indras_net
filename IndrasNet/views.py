# from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .models import Model
from .models import ModelParam

from .forms import MainForm

from indra.api import get_agent

#RUN = 'run'
#STEP = 'step'
#SHOW = 'show'
MODEL = 'model'
HEADER = 'header'

def get_hdr():
    site_hdr = "Indra's Net: an agent-based modeling system."
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
    site_hdr = get_hdr()
    model_name = request.POST[MODEL]
    model = Model.objects.get(name=model_name)
    print("-----------")
    print(model.params.all())
    
    template_data = {'model': model, HEADER: site_hdr}
    return render(request, 'parameters.html', template_data)

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
