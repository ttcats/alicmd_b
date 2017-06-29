# coding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth

from django.db.models import Q
from opera.models import mysql_info, mysql_db_info
import json
import commands
import multiprocessing
import time



@login_required
@csrf_exempt
def db_info(request):
    if request.method == "GET":
        print(request.GET)
        if request.GET.keys() == []:
            return render(request, 'opera/db_info.html', locals())
        else:
            search = request.GET['search'] if 'search' in request.GET.keys() else ''
            limit = request.GET['limit'] if 'limit' in request.GET.keys() else 20
            offset = request.GET['offset'] if 'offset' in request.GET.keys() else 0
            print(limit,offset,search)
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
        print(db_info_old)
        print(request.POST)
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
            print(info_del,info_add,'diff')
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
        search = request.GET['search'] if 'search' in request.GET.keys() else ''
        limit = request.GET['limit'] if 'limit' in request.GET.keys() else 20
        offset = request.GET['offset'] if 'offset' in request.GET.keys() else 0
        limits = int(limit) + int(offset)
        contact_list = mysql_db_info.objects.filter(~Q(status=0))
        messages,messages_search = [],[]
        for contact in contact_list:
            messages.append({"hostname":contact.hostname,"db":contact.dbname,"port":contact.port,"info":contact.db_info})
        try:
            #设置可查询类型
            if messages:
                for message in messages:
                    if search in str(message['db']):
                        messages_search.append(message)
                    elif search in str(message['hostname']):
                        messages_search.append(message)
            total = len(messages_search)
            messages_all = messages_search[int(offset):int(limits)]
            s = {"total":total,"rows":messages_all}
            t=json.dumps(s,indent=4,cls=DjangoJSONEncoder)
        except exception as e:
            t = []
            print(e)
        return HttpResponse(t)
    elif request.method == "POST":
        con = eval(request.POST['strJson'])
        print(con,type(con))
        try:
            mysql_db_info.objects.filter(hostname=con['hostname'], dbname=con['db'],port=con['port']).update(db_info=con['info'])
            return HttpResponse('sucess')
        except exception as e:
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
             except exception as e:
                 print(e)
                 return HttpResponse('err')

        else:
            return HttpResponse('notchoice')


@login_required
@csrf_exempt
def dbinfo_change(request):
   if request.method == "POST":
       print(request.POST)
  
       hostname =  request.POST.get('hostname')
       port =  request.POST.get('port')
       group_id =  request.POST.get('group_id')
       m_hostname =  request.POST.get('m_hostname')
       m_port =  request.POST.get('m_port')
       try:
           mysql_info.objects.create(hostname=hostname,port=port,group_id=group_id,m_hostname=m_hostname,m_port=m_port)
           return HttpResponse('sucess')
       except exception as e:
           print(e)
           return HttpResponse('err')
   elif request.method == "GET":
       print(request.GET)
       con = eval(request.GET['strJson'])
       try:
           mysql_info.objects.filter(hostname=con['hostname']).update(port=con['port'])
           return HttpResponse('sucess')
       except exception as e:
           print(e)
           return HttpResponse('err')


@login_required
def db_messages(request):
    if request.method == "GET":
        search = request.GET['search'] if 'search' in request.GET.keys() else ''
        limit = request.GET['limit'] if 'limit' in request.GET.keys() else 20
        offset = request.GET['offset'] if 'offset' in request.GET.keys() else 0
        limits = int(limit) + int(offset)

        contact_list = mysql_db_info.objects.filter(~Q(status=2))

        messages,messages_search = [],[]
        try:
            for contact in contact_list:
                if int(contact.status) == 1:
                    messages.append({"message":"新增数据库 :主机: "+contact.hostname+" 端口: "+str(contact.port)+" 数据库: "+contact.dbname,"time":contact.createtime})
                elif int(contact.status) == 0:
                    messages.append({"message":"删除数据库 :主机: "+contact.hostname+" 端口: "+str(contact.port)+" 数据库: "+contact.dbname,"time":contact.createtime})
        except exception as e:
            print(e)
            pass

        try:
            if messages:
                for message in messages:
                    if search in str(message['message']):
                        messages_search.append(message)
                    elif search in str(message['time']):
                        messages_search.append(message)
            total = len(messages_search)
            messages_all = messages_search[int(offset):int(limits)]
            s = {"total":total,"rows":messages_all}
            t=json.dumps(s,indent=4,cls=DjangoJSONEncoder)
        except exception as e:
            t = []
            print(e)
        return HttpResponse(t)



@login_required
@csrf_exempt
def db_opera(request):
    if request.method == "GET":
        host_lists = mysql_info.objects.filter(status=True)
        dbs = [[str(x.hostname),str(x.port)] for x in host_lists]
        return render(request, 'opera/db_opera.html', locals())
    elif request.method == "POST":
        print(request.POST)
        db_info = request.POST.get('db','')
        databa = []
        if db_info != '':
            #SHOW_SQL = "/usr/bin/mysql -ur_cmdb_check -pcmdb@sh7*sheja -h%s -P%s -e 'show databases\G;' |awk '/Database/{print $2}' " %(db_info.split("'")[1],db_info.split("'")[3])
            SHOW_SQL = "/usr/bin/mysql -uroot -p123 -h127.0.0.1 -P3306 -e 'show databases\G;' 2>/dev/null|awk '/Database/{print $2}' " 
            print(SHOW_SQL)
            (status, output) = commands.getstatusoutput(SHOW_SQL)
            if status == 0:
                for db in output.split():
                    databa.append(db)
        msg = json.dumps(databa,sort_keys=True,indent=4)
        print(msg)
        return HttpResponse(msg)



@login_required
def mysql_command(host,user,passwd,db,port,sql,queues):
    queues.put(os.getpid())  #子进程
    try:
        ret = {}
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,port=port,charset="utf8",cursorclass=MySQLdb.cursors.DictCursor)
        cursor = conn.cursor()
        start = time.time()
        cursor.execute(sql)
        conn.commit()
        ret['time']=round(time.time()-start,5)
        ret['line']= cursor.rowcount
        ret['export'] = [x for x in cursor.fetchall()]
    except MySQLdb.Error as e:
        conn.rollback()
        ret['export'] = e

    queues.put(ret) #结果





@csrf_exempt
@login_required
def db_query(request):
    if request.method == "POST":
        print(request.POST)
        db = request.POST.get('db')
        databa = request.POST.get('databa')
        sql = request.POST.get('sql')
        queues = multiprocessing.Queue()
        threads = multiprocessing.Process(target=mysql_command, args=('127.0.0.1','root','123','oms',3306,sql,queues))
        threads.daemon = True
        threads.start()
        time.sleep(1)

        #获取PID和运行结果
        try:
            while True:
                if not queues.empty():
                    PID = queues.get()
                    sql_status.objects.create(sql_h=conf.get("db","host"),sql_r=sql,pid_r=PID)
                    break
                else:
                    time.sleep(1)

            while True:
                if not queues.empty():
                    comms = queues.get()
                    break
                else:
                    sql_kill = sql_status.objects.filter(sql_h=conf.get("db","host"),sql_r=sql,pid_r=PID,status_r=True)
                    print(sql_kill,type(sql_kill))
                    lis_sql = [ x for x in sql_kill]
                    print(lis_sql,'---',type(lis_sql),len(lis_sql))
                    if len(lis_sql) != 0:
                        val = "Kill %s" %sql
                        print(PID,type(PID))
                        kill_stat = os.system('kill -9 %s' %PID)
                        if kill_stat == 0:
                            comms = {"export": val}
                        else:
                            comms = {"export": "ERROR"}
                            print(comms,'kill')
                            break
                    else:
                        time.sleep(1)

            sql_status.objects.filter(sql_h=conf.get("db","host"),sql_r=sql,pid_r=PID).delete()
        except Exception as e:
            comms = {"export": e}

        #db_connect = db_oper(conf.get("db","host"),conf.get("db","user"),conf.get("db","pass"),'oms',3306,sql)
        #comms = db_connect.mysql_command()
        print(comms,'comms')
        try:
            #显示排版
            table_tds = ''
            for comm in comms['export']:
                titles = comm.keys()
                titles.reverse()
                table_td = ''
                for c_key in titles:
                    c_value = "<td>" + str(comm[c_key]) + "</td>"
                    table_td = c_value + table_td
                    table_tds = "<tr>" + table_td + "</tr>" + table_tds
                table_ths = ''
                for c_key in titles:
                    table_th = "<th>" + str(c_key) + "</th>"
                    table_ths = table_th + table_ths
            table_html = "<table id='msg'> <tr>%s</tr>%s</table><p>%s rows in set (%s sec)</p>" % (table_ths,table_tds,comms['line'],comms['time'])
        except Exception as e:
            print(e)
            table_html = "<p class='bg-warning'>" + str(comms['export']) + "</p>"
        return HttpResponse(table_html)




@login_required
@csrf_exempt
def sql_kill(request):
    if request.method == "POST":
        print(request.POST)
        host = request.POST.get('db')
        sql = request.POST.get('sql')
        try:
            sql_status.objects.filter(sql_h='localhost',sql_r=sql).update(status_r=True)
            return HttpResponse('sucess')
        except Exception as e:
            print(e)
            return HttpResponse('error')




