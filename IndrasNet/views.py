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
    text_for_box2 = ''
    
    #Load module
    model_name = request.POST[MODEL]
    model = Model.objects.get(name=model_name)
    module = model.module
    importlib.import_module(module[0:-4])
    
    questions = model.params.all()
    
    #Take actions on a running model
    if(action):
        prop_dic = {}
        for q in questions:
            value = q.default_val
            if q.atype == "INT":
                value = int(value)
            elif q.atype == "DBL":
                value = float(value)
            prop_dic[q.prop_name] = value
        
        env = eval(module + "(prop_dic)")
        env.restore_session(session_id)
        
        if action == "step":            
            env.run(1)

        if action == "n_steps":
            steps = int(request.POST["steps"])
            env.run(steps)

        if action == "list_agents":
            env.list_agents()
            text_for_box2 = env.user.text_output.split("Active agents in environment:")[0]
        if action == "properties":
            text_for_box2 = env.props.display()
        # if action == "view_pop":
        #     #     if env.period < 4:
        #     #         text_for_box2 = "Too little data to display"
        env.save_session(session_id)
        
    #Run a model for the first time
    else:
        answers = {}
        for q in questions:
            answer = request.POST[q.question]
            if q.atype == "INT":
                answer = int(answer)
            elif q.atype == "DBL":
                answer = float(answer)
            # Boolen is not considered yet
            answers[q.prop_name] = answer
        env = eval(module + "(answers)")
        env.save_session(session_id)
              
    site_hdr = get_hdr()

    text, image_bytes = env.user.text_output, env.image_bytes
    image = base64.b64encode(image_bytes.getvalue()).decode()
    index1 = env.user.text_output.find("Ran for")
    index2 = env.user.text_output.find("Census:")
    text_for_box1 = env.user.text_output[index1:index2]
    
    template_data = { HEADER: site_hdr, 'text': text_for_box1, 'image': image,
                     'text2': text_for_box2, 'model': model}
    
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
