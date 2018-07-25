from django.db import models

HEADER_LEN = 64

ATYPE_CHOICES = (
    ('', ''),
    ('INT', 'Integer'),
    ('DBL', 'Double'),
    ('BOOL', 'Boolean'),
    ('STR', 'String'),
)


class SingleNameModel(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class UrlModel(models.Model):
    url = models.CharField(max_length=512, default="",
                           blank=True, null=True)

    class Meta:
        abstract = True


class DescrModel(models.Model):
    descr = models.CharField(max_length=512, default="", blank=True,
                             null=True)

    class Meta:
        abstract = True


class AdminEmail(models.Model):
    email_addr = models.CharField(max_length=80, default="", blank=True, null=True)

    def __str__(self):
        return self.email_addr


# this model captures site specific info
class Site(SingleNameModel, UrlModel, DescrModel):
    header = models.CharField(max_length=HEADER_LEN, default="")


class ModelType(SingleNameModel, DescrModel):
    pass


class ModelParam(models.Model):
    question = models.CharField(max_length=128)
    atype = models.CharField(choices=ATYPE_CHOICES, max_length=12)
    default_val = models.CharField(max_length=16, null=True, default="",
                                   blank=True)
    lowval = models.FloatField(blank=True, null=True)
    hival = models.FloatField(blank=True, null=True)
    prop_name = models.CharField(max_length=16, default="prop_default")

    def __str__(self):
        return self.question


class Model(SingleNameModel, DescrModel):
    mtype = models.ForeignKey(ModelType, models.SET_NULL, null=True, )
    module = models.CharField(max_length=128)
    functional = models.BooleanField(default=False)
    params = models.ManyToManyField(
        ModelParam, default="", related_name="parameters", blank=True,
    )
