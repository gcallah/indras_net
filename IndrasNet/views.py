# from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .forms import MainForm

CODE = 'code'
NXT_KEY = 'nxt_key'
STEP = 'step'
CLEAR = 'clear'
HEADER = 'header'


def get_hdr():
    site_hdr = "Thomas's Net: an agent-based modeling system."
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

    if request.method == 'GET':
        form = MainForm()
    else:
        form = MainForm(request.POST)
    return render(request, 'main.html',
                  {'form': form,
                   HEADER: site_hdr
                  })

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
