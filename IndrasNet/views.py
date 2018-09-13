# from collections import OrderedDict

import logging
import importlib
import sys

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .models import Model
from .models import ModelParam
from django import forms

import models
import schelling
import wolfram
import bigbox
import base64

# Need this for using a global vaiable in it. Only for testing

logger = logging.getLogger(__name__)

MODEL = 'model'
HEADER = 'header'
ACTION = 'action'
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

    model_list = Model.objects.order_by('mtype')
    template_data = {'models': model_list, HEADER: site_hdr}
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

    # Assign a new session id to a new user
    assign_key(request)

    site_hdr = get_hdr()
    model_name = request.GET[MODEL]
    model = Model.objects.get(name=model_name)
    form = ParamForm(questions=model.params.all())

    template_data = {'form': form, HEADER: site_hdr, 'model': model}
    return render(request, 'parameters.html', template_data)

def run(request):
            
    try:
        action = request.POST[ACTION]
    except KeyError:
        action = None

    
    session_id = int(request.session['session_id'])
    
    #Load module
    model_name = request.POST[MODEL]
    model = Model.objects.get(name=model_name)
    module = model.module
    plot_type = model.plot_type
    importlib.import_module(module[0:-4])
    
    questions = model.params.all()
    
    #Take actions on a running model
    if(action):
        prop_dict = {}
        for q in questions:
            value = q.default_val
            if q.atype == "INT":
                value = int(value)
            elif q.atype == "DBL":
                value = float(value)
            prop_dict[q.prop_name] = value

        env = eval(module + "(prop_dict)")
        env.restore_session(session_id)
        
        #CLear textboxs except for the first one
        for i in range(len(env.user.text_output)):
            if i != 0:
                env.user.text_output[i] = ''
        #Tools
        if action == "step":            
            env.step()

        if action == "n_steps":
            steps = int(request.POST["steps"])
            env.n_steps(steps)

        #View
        if action == "list_agents":
            env.list_agents()
            
        if action == "properties":
            env.user.text_output[1] = env.props.display()
        
        #File
        if action == "disp_log":
            env.disp_log()
            
        #Edit
        if action == "add":
            pass

        env.save_session(session_id)
        
    #Run a model for the first time
    else:
        answers = {}
        answers["plot_type"] = plot_type
        for q in questions:
            answer = request.POST[q.question]
            if q.atype == "INT":
                answer = int(answer)
            elif q.atype == "DBL":
                answer = float(answer)
            # Boolean is not considered yet
            answers[q.prop_name] = answer
        print("here")
        print("module: " + module)
        env = eval(module + "(answers)")
        env.save_session(session_id)
              
    site_hdr = get_hdr()

    text_box, image_bytes = env.user.text_output, env.plot()
    image = base64.b64encode(image_bytes.getvalue()).decode()
    
    template_data = { HEADER: site_hdr, 'text0': text_box[0], 'image': image,
                     'text1': text_box[1], 'model': model}
    
    return render(request, 'run.html', template_data)

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

def about(request):

    site_hdr = get_hdr()
    return render(request, 'about.html', {HEADER: site_hdr})

def assign_key(request):
    if 'session_id' not in request.session:

        with open("session_id.txt", "w+") as f:
            session_id = f.readline()
            if not session_id:
                session_id = 0
            else:
                session_id = int(session_id)
            session_id += 1
            new_id = session_id
            f.write(str(session_id))

        request.session['session_id'] = new_id
        request.session.modified = True

    else:
        logging.info("This user has a session id: ", request.session['session_id'])
