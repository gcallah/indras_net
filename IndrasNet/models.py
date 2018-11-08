"""
    models.py:
        this creates the models necessary for the Indra system.
"""
from django.db import models

HEADER_LEN = 64

ATYPE_CHOICES = (
    ('', ''),
    ('INT', 'Integer'),
    ('DBL', 'Double'),
    ('BOOL', 'Boolean'),
    ('STR', 'String'),
)

PLOT_CHOICES = (
    ('NO', 'None'),
    ('SC', 'Scatterplot'),
    ('LN', 'Line'),
)


class SingleNameModel(models.Model):
    """
        All models with a single 'main' name can inherit from this class.
    """
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        """
            This registers the fact that SingleNameModel is a Meta class.
        """
        abstract = True
        ordering = ['name']


class UrlModel(models.Model):
    """
        All models that contain a URL field can inherit from this class.
    """
    url = models.CharField(max_length=512, default="",
                           blank=True, null=True)

    class Meta:
        """
            This registers the fact that UrlModel is a Meta class.
        """
        abstract = True


class DescrModel(models.Model):
    """
        All models with a description field can inherit from this class.
    """
    descr = models.CharField(max_length=512, default="", blank=True,
                             null=True)

    class Meta:
        """
            This registers the fact that DescrModel is a Meta class.
        """
        abstract = True


class AdminEmail(models.Model):
    """
        This model is for an admin email table. Maybe not needed?
    """
    email_addr = models.CharField(max_length=80,
                                  default="", blank=True, null=True)

    def __str__(self):
        return self.email_addr


class Site(SingleNameModel, UrlModel, DescrModel):
    """
        This model captures site specific info.
    """
    header = models.CharField(max_length=HEADER_LEN, default="")


class ModelType(SingleNameModel, DescrModel):
    """
        This model does nothing right now: do we know why it is here?
    """
    pass


class ModelParam(models.Model):
    """
        This is a table of what possible questions might
        need to be answered to set a model's parameters.
    """
    question = models.CharField(max_length=128)
    atype = models.CharField(choices=ATYPE_CHOICES, max_length=12)
    default_val = models.CharField(max_length=16, null=True, default="",
                                   blank=True)
    lowval = models.FloatField(blank=True, null=True)
    hival = models.FloatField(blank=True, null=True)
    prop_name = models.CharField(max_length=16, default="prop_default")

    def __str__(self):
        return self.question


class ABMModel(SingleNameModel, DescrModel):
    """
        This table describes each model available in Indra.
    """
    mtype = models.ForeignKey(ModelType, models.SET_NULL, null=True, )
    module = models.CharField(max_length=128)
    disp_name = models.CharField(max_length=130)
    functional = models.BooleanField(default=False)
    plot_type = models.CharField(choices=PLOT_CHOICES, max_length=2,
                                 blank=False, null=True, default=None)
    params = models.ManyToManyField(
        ModelParam, default="", related_name="parameters", blank=True,
    )
