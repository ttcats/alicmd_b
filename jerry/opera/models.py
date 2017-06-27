#coding: utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.



class mysql_info(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.CharField(max_length=10,null=True,blank=True,verbose_name=u'组ID')
    hostname = models.CharField(max_length=100,verbose_name=u'主机')
    port = models.CharField(max_length=50,verbose_name=u'端口')
    m_hostname = models.CharField(max_length=100,null=True,blank=True,verbose_name=u'所属组MASTER')
    m_port = models.CharField(max_length=100,null=True,blank=True,verbose_name=u'MASTER端口')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    status = models.BooleanField(default=True,verbose_name=u'数据库状态')

    def __unicode__(self):
        return "%s    %s" %(self.hostname,self.port)
    class Meta:
        verbose_name = u'数据库信息'
        verbose_name_plural = u'数据库信息'



class mysql_db_info(models.Model):
    id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=100,verbose_name=u'主机')
    port = models.CharField(max_length=50,verbose_name=u'端口')
    dbname = models.CharField(max_length=100,verbose_name=u'数据库')
    db_info = models.CharField(max_length=300,null=True,verbose_name=u'备注信息')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    status = models.CharField(max_length=10,null=True,verbose_name=u'Databas状态,1表示增,0表示删')

    def __unicode__(self):
        return self.hostname
    class Meta:
        verbose_name = u'db信息'
        verbose_name_plural = u'db信息'

