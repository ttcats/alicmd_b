from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Jobs(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'job')
    jobtype = models.CharField(max_length=32, verbose_name=u'jobtype')
    inventory = models.CharField(max_length=256, verbose_name=u'inventory')
    project = models.CharField(max_length=32, verbose_name=u'project')
    playbook = models.CharField(max_length=128)
    forks = models.IntegerField(blank=True, default='', null=True)
    create_time = models.DateField(auto_now=True, null=True)
    create_author = models.CharField(max_length=64)
    jobs_status = models.BooleanField()
    

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Jobs"
        verbose_name_plural = verbose_name
