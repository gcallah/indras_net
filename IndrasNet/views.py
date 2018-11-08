"""
    This file implements the views for our web-based
    agent modelling system.
"""

import logging
import importlib
import base64
import models  # noqa F401
import schelling  # noqa F401
import wolfram  # noqa F401
import bigbox  # noqa F401

from django.shortcuts import render
from django import forms

from .models import ABMModel, AdminEmail


logger = logging.getLogger(__name__)

STR = "STR"
INT = "INT"
DBL = "DBL"
BOOL = "BOOL"

MODEL = 'model'
HEADER = 'header'
ACTION = 'action'
DEFAULT_HIGHVAL = 100000
DEFAULT_LOWVAL = 0


def get_hdr():
    """
        This gets the site header: one day, we may have a dev version
        of the server, and we may have different headers then.
    """
    site_hdr = "Indra's Net"
    return site_hdr


def index(request):
    """
        This renders the index page of the site.
    """
    site_hdr = get_hdr()

    template_data = {HEADER: site_hdr}

    return render(request, 'main.html', template_data)


def ab_models(request):
    """
        This is the view of all of our agent-based models.
    """
    site_hdr = get_hdr()

    model_list = ABMModel.objects.order_by('mtype')
    template_data = {'models': model_list, HEADER: site_hdr}
    return render(request, 'abmodels.html', template_data)


def parameters(request):
    """
        This view renders our parameters for a model.
    """
    class ParamForm(forms.Form):
        """
            And this class implements the parameters in a form.
        """
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
                if q.atype == STR:
                    self.fields[q.question] = forms.CharField(label=q.question,
                                                           initial=default,
                                                           max_length=20)
                elif q.atype == INT:
                    self.fields[q.question] = forms.IntegerField(label=q.question,
                                                              initial=default,
                                                              min_value=lowval,
                                                              max_value=hival)
                elif q.atype == DBL:
                    self.fields[q.question] = forms.FloatField(label=q.question,
                                                            initial=default,
                                                            min_value=lowval,
                                                            max_value=hival)
                elif q.atype == BOOL:
                    self.fields[q.question] = forms.BooleanField(label=q.question,
                                                                 required=False)
    # Assign a new session id to a new user
    assign_key(request)

    model = ABMModel.objects.get(name=request.GET[MODEL])
    form = ParamForm(questions=model.params.all())

    template_data = {'form': form, HEADER: get_hdr(), 'model': model}
    return render(request, 'parameters.html', template_data)


def run(request):
    """
        This runs the model that was picked.
    """
    env = None
    try:
        action = request.POST[ACTION]
    except KeyError:
        action = None

    session_id = int(request.session['session_id'])

    # Load entry_point
    model_name = request.POST[MODEL]
    model = ABMModel.objects.get(name=model_name)
    entry_point = model.module
    plot_type = model.plot_type
    importlib.import_module(entry_point[0:-4])

    questions = model.params.all()

    # Take actions on a running model
    if action:
        env = running_model(request, action, entry_point,
                            questions, session_id)
    # Run a model for the first time
    else:
        env = model_first_run(request, action, entry_point, questions,
                              session_id, plot_type)

    site_hdr = get_hdr()

    text_box, image_bytes = env.user.text_output, env.plot()
    image = base64.b64encode(image_bytes.getvalue()).decode()

    template_data = {HEADER: site_hdr, 'text0': text_box[0], 'image': image,
                     'text1': text_box[1], 'model': model}

    return render(request, 'run.html', template_data)


def running_model(request, action, entry_point, questions, session_id):
    prop_dict = {}
    for q in questions:
        value = q.default_val
        if q.atype == "INT":
            value = int(value)
        elif q.atype == "DBL":
            value = float(value)
        prop_dict[q.prop_name] = value

    env = eval(entry_point)(prop_dict)
    env.restore_session(session_id)

    # Clear textboxes except for the first one
    for i in range(len(env.user.text_output)):
        if i != 0:
            env.user.text_output[i] = ''
    # Tools
    if action == "step":
        env.step()

    if action == "n_steps":
        steps = int(request.POST["steps"])
        env.n_steps(steps)

    # View
    if action == "list_agents":
        env.list_agents()

    if action == "properties":
        env.user.text_output[1] = env.props.display()

    # File
    if action == "disp_log":
        env.disp_log()

    # Edit
    if action == "add":
        pass

    env.save_session(session_id)
    return env


def model_first_run(request, action, entry_point, questions, session_id,
                    plot_type):
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
    env = eval(entry_point)(answers)
    # env = entry_point(answers)
    env.save_session(session_id)
    return env


def help_page(request):
    """
        This function renders our help page.
    """
    site_hdr = get_hdr()
    return render(request, 'help.html', {HEADER: site_hdr})


def feedback(request):
    """
        This function renders our feedback page.
    """
    site_hdr = get_hdr()
    email_list = AdminEmail.objects.all()
    comma_del_emails = ""
    for email in email_list:
        comma_del_emails = comma_del_emails + email.email_addr + ","
    comma_del_emails = comma_del_emails[:-1]
    return render(request, 'feedback.html', {'emails': comma_del_emails,
                                             HEADER: site_hdr})


def about(request):
    """
        This function renders our about page.
    """
    site_hdr = get_hdr()
    return render(request, 'about.html', {HEADER: site_hdr})


def assign_key(request):
    """
        Assign a key to a user.
    """
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
        logging.info("This user has a session id: ",
                     request.session['session_id'])
