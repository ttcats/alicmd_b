# coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Q
from opera.models import mysql_info, mysql_db_info
import json





@login_required
@csrf_exempt
def db_info(request):
    if request.method == "GET":
        print request.GET.keys()
        if request.GET.keys() == []:
            return render(request, 'opera/db_info.html', locals())
        else:
            if 'search' in request.GET.keys():
                search = request.GET['search']
            else:
                search = ''
            if 'limit' in request.GET.keys():
                limit = request.GET['limit']
            else:
                limit = 20
            if 'offset' in request.GET.keys():
                offset = request.GET['offset']
            else:
                offset = 0
            print limit,offset,search
            limits = int(limit) + int(offset)

            contact_list = mysql_info.objects.filter(status=True)
            messages,messages_search = [],[]
            for contact in contact_list:
                messages.append({"hostname":contact.hostname,"port":contact.port,"group_id":contact.group_id,"m_hostname":contact.m_hostname,"m_port":contact.m_port,"hostid":contact.id})
            #设置可查询类型
            if messages == []:
                t = []
            else:
                for message in messages:
                    if search in str(message['hostname']):
                        messages_search.append(message)

            total = len(messages_search)
            messages_all = messages_search[int(offset):int(limits)]
            s = {"total":total,"rows":messages_all}

            t=json.dumps(s,indent=4,cls=DjangoJSONEncoder)
            return HttpResponse(t)

    elif request.method == "POST":
        #mysql_db_info.objects.all().delete()
        db_info_old = [ [x.hostname,x.port,x.dbname] for x in mysql_db_info.objects.all() ]
        print db_info_old
        print request.POST
        contact_list = mysql_info.objects.filter(status=True)
        db_info_new = []
        for contact in contact_list:
            SHOW_SQL = "/usr/bin/mysql -ur_cmdb_check -pcmdb@sh7*sheja -h%s -P%s -e 'show databases\G;' |awk '/Database/{print $2}' " %(contact.hostname,contact.port)
            (status, output) = commands.getstatusoutput(SHOW_SQL)
            if status == 0:
                for db in output.split():
                    db_info_new.append([contact.hostname,contact.port,db])
        print(db_info_new)

        if len(db_info_new) == 0:
            return HttpResponse("ERROR")
        elif len(db_info_old) == 0 and len(db_info_new) != 0:
            for info in db_info_new:
                 mysql_db_info.objects.create(hostname=info[0],port=info[1],dbname=info[2],status=2)
        elif len(db_info_old) != 0 and len(db_info_new) != 0:
            info_del = [d for d in db_info_old if d not in db_info_new]
            info_add = [a for a in db_info_new if a not in db_info_old]
            print info_del,info_add,'diff'
            if len(info_del) != 0:
                for info_d in info_del:
                    mysql_db_info.objects.filter(hostname=info_d[0],port=info_d[1],dbname=info_d[2]).update(status=0)
            if len(info_add) != 0:
                for info_a in info_add:
                    mysql_db_info.objects.create(hostname=info_a[0],port=info_a[1],dbname=info_a[2],status=1)

        return HttpResponse("success")



@login_required
@csrf_exempt
def dbtable_info(request):
    if request.method == "GET":
        if 'search' in request.GET.keys():
            search = request.GET['search']
        else:
            search = ''
        if 'limit' in request.GET.keys():
            limit = request.GET['limit']
        else:
            limit = 20
        if 'offset' in request.GET.keys():
            offset = request.GET['offset']
        else:
            offset = 0
        print limit,offset,search
        limits = int(limit) + int(offset)

        contact_list = mysql_db_info.objects.filter(~Q(status=0))
        messages,messages_search = [],[]
        for contact in contact_list:
            messages.append({"hostname":contact.hostname,"db":contact.dbname,"port":contact.port,"info":contact.db_info})
        #设置可查询类型
        if messages == []:
            t = []
        else:
            for message in messages:
                if search in str(message['db']):
                    messages_search.append(message)
                elif search in str(message['hostname']):
                    messages_search.append(message)

        total = len(messages_search)
        messages_all = messages_search[int(offset):int(limits)]
        s = {"total":total,"rows":messages_all}

        t=json.dumps(s,indent=4,cls=DjangoJSONEncoder)
        #print t
        return HttpResponse(t)
    elif request.method == "POST":
        con = eval(request.POST['strJson'])
        print con,type(con)
        try:
            mysql_db_info.objects.filter(hostname=con['hostname'], dbname=con['db'],port=con['port']).update(db_info=con['info'])
            return HttpResponse('sucess')
        except exception,e:
            return HttpResponse(e)



@login_required
def dbinfo_remove(request):
    if request.method == "GET":
        if len(request.GET.keys()) == 2:
             hostids = request.GET.getlist('values[]')
             try:
                 for hostid in hostids:
                     mysql_info.objects.filter(id=hostid).update(status=False)
                 return HttpResponse('success')
             except exception,e:
                 print e
                 return HttpResponse('err')

        else:
            return HttpResponse('notchoice')


@login_required
@csrf_exempt
def dbinfo_change(request):
   if request.method == "POST":
       print request.POST
  
       hostname =  request.POST.get('hostname')
       port =  request.POST.get('port')
       group_id =  request.POST.get('group_id')
       m_hostname =  request.POST.get('m_hostname')
       m_port =  request.POST.get('m_port')
       try:
           mysql_info.objects.create(hostname=hostname,port=port,group_id=group_id,m_hostname=m_hostname,m_port=m_port)
           return HttpResponse('sucess')
       except exception,e:
           print e
           return HttpResponse('err')
   elif request.method == "GET":
       print request.GET
       con = eval(request.GET['strJson'])
       try:
           mysql_info.objects.filter(hostname=con['hostname']).update(port=con['port'])
           return HttpResponse('sucess')
       except exception,e:
           print e
           return HttpResponse('err')


@login_required
def db_messages(request):
    if request.method == "GET":
        if 'search' in request.GET.keys():
            search = request.GET['search']
        else:
            search = ''
        if 'limit' in request.GET.keys():
            limit = request.GET['limit']
        else:
            limit = 20
        if 'offset' in request.GET.keys():
            offset = request.GET['offset']
        else:
            offset = 0
        print limit,offset,search,'message'
        limits = int(limit) + int(offset)

        contact_list = mysql_db_info.objects.filter(~Q(status=2))

        messages,messages_search = [],[]
        try:
            for contact in contact_list:
                if int(contact.status) == 1:
                    messages.append({"message":"新增数据库 :主机: "+contact.hostname+" 端口: "+str(contact.port)+" 数据库: "+contact.dbname,"time":contact.createtime})
                elif int(contact.status) == 0:
                    messages.append({"message":"删除数据库 :主机: "+contact.hostname+" 端口: "+str(contact.port)+" 数据库: "+contact.dbname,"time":contact.createtime})
        except exception,e:
            pass

        if messages == []:
            t = []
        else:
            for message in messages:
                if search in str(message['message']):
                    messages_search.append(message)
                elif search in str(message['time']):
                    messages_search.append(message)

        total = len(messages_search)
        messages_all = messages_search[int(offset):int(limits)]
        s = {"total":total,"rows":messages_all}

        t=json.dumps(s,indent=4,cls=DjangoJSONEncoder)
        #print t,'messages'
        return HttpResponse(t)


