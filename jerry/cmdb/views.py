from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .Ansible_api import Runner
import  json

from cmdb.models import Asset, IDC, AssetGroup, ASSET_TYPE, ASSET_STATUS, ASSET_ENV



def aliyunecs(request):
    return render(request, 'cmdb/aliyunecs.html')

def asset(request):
    search = request.GET.get('search')
    page = request.GET.get('page')
    #print(search)
    assets = Asset.objects.all()
    Search = ''
    if search:
        assets = Asset.objects.filter(Q(hostname__icontains=search)|Q(ip__icontains=search))
        Search = "&search=" + search

    paginator = Paginator(assets, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    
    number_list=range(1,contacts.paginator.num_pages + 1)
    print(contacts.paginator.num_pages,'total_page')
    #return render(request, 'cmdb/asset.html',{'assets': assets})
    return render(request, 'cmdb/asset.html',{'contacts': contacts,'Search': Search, 'number_list': number_list})



@csrf_exempt
@login_required
def asset_edit(request):
    if request.method == 'POST':
        print(request.POST)
        hostname = request.POST.get('hostname','')
        host_ip = request.POST.get('host_ip','')
        ssh_port = request.POST.get('ssh_port','')
        idc = request.POST.get('idc','')
        remote_ip = request.POST.get('remote_ip','')
        mac = request.POST.get('mac','')
        brand = request.POST.get('brand','')
        cpu = request.POST.get('cpu','')
        memory = request.POST.get('memory','')
        disk = request.POST.get('disk','')
        system_type = request.POST.get('system_type','')
        system_version = request.POST.get('system_version','')
        system_arch = request.POST.get('system_arch','')
        number = request.POST.get('number','')
        sn = request.POST.get('sn','')
        cabinet = request.POST.get('cabinet','')
        comment = request.POST.get('comment','')
        asset_type = request.POST.get('asset_type','')
        asset_env = request.POST.get('asset_env','')
        asset_status = request.POST.get('asset_status','')
        groups = request.POST.get('groups','')
        is_active = True if request.POST.get('is_active') == 'on' else False

        try:
            host_id = request.get_full_path().split('=')[1]
            if Asset.objects.get(id=host_id):
                if hostname != Asset.objects.get(id=host_id).hostname and Asset.objects.filter(hostname=hostname):
                    mess = u'该主机名 %s 已存在!' % hostname
                else:
                    Asset.objects.filter(id=host_id).update(hostname=hostname,ip=host_ip,port=ssh_port,idc=IDC.objects.get(id=idc),remote_ip=remote_ip,\
                                                            mac=mac,brand=brand,cpu=cpu,memory=memory,disk=disk,number=number,sn=sn,\
                                                            system_type=system_type,system_version=system_version,system_arch=system_arch,\
                                                            cabinet=cabinet,comment=comment,asset_type=asset_type,env=asset_env,status=asset_status,is_active=is_active)
                    assetsave = Asset.objects.get(id=host_id)
                    assetsave.group.clear()
                    for groupid in groups.strip().split(' '):
                        group = AssetGroup.objects.get(id=groupid)
                        assetsave.group.add(group)
                    mess = 'Add.True'
                #else:
                #    if Asset.objects.filter(hostname=hostname):
                #        mess = u'该主机名 %s 已存在!' % hostname
                #    else:
                #        Asset.objects.filter(id=host_id).update(hostname=hostname,ip=host_ip,port=ssh_port,idc=IDC.objects.get(id=idc),remote_ip=remote_ip,mac=mac,brand=brand,cpu=cpu,memory=memory,disk=disk,number=number,sn=sn,system_type=system_type,system_version=system_version,system_arch=system_arch,cabinet=cabinet,comment=comment,asset_type=asset_type,env=asset_env,status=asset_status,is_active=is_active)
                #        assetsave = Asset.objects.get(id=host_id)
                #        assetsave.group.clear()
                #        for groupid in groups.strip().split(' '):
                #            group = AssetGroup.objects.get(id=groupid)
                #            assetsave.group.add(group)
                #        mess = 'Add.True'
        except ValueError as e:
            print(e,'ValueError')
            mess = '请重新点击编辑!'
        except Exception as e:
            print(e,'2')
            mess = e
        return HttpResponse(mess)
    else:
        asset_id = request.GET.get('id','')
        asset_group_all = AssetGroup.objects.all() 
        asset_idc_all = IDC.objects.all() 
        asset_type,asset_env,asset_status = ASSET_TYPE, ASSET_ENV, ASSET_STATUS
        try:
            asset = Asset.objects.get(id=asset_id)
            groups = [ info.name for info in asset.group.all() ]
        
            return render(request, 'cmdb/asset_edit.html',{'asset_group_all': asset_group_all,
                                                           'asset_idc_all': asset_idc_all, 
                                                           'asset_type': asset_type, 
                                                           'asset_env': asset_env, 
                                                           'asset_status': asset_status, 
                                                           'asset': asset, 
                                                           'groups': groups})
        except Exception as e:
            print(e)
            return render(request, 'cmdb/asset_edit.html',{'asset_group_all': asset_group_all,
                                                           'asset_idc_all': asset_idc_all, 
                                                           'asset_type':asset_type,
                                                           'asset_env': asset_env, 
                                                           'asset_status': asset_status})



def asset_del(request):
    asset_id = request.GET.get('id','')
    print(asset_id)
    try:
        asset = Asset.objects.get(id=asset_id).delete()
        return HttpResponse('true')
    except Exception as e:
        print(e)
        return HttpResponse('error')
    
def asset_update(request):
    print(request.GET)
    asset_id = request.GET.get('id')
    asset = Asset.objects.get(id=asset_id)
    asset_ip = asset.ip
    print(asset_ip)
    #asset_ip = '10.7.253.113'

    ansi_api = Runner()
    try:
        asset_info = json.loads(ansi_api.run(asset_ip, 'setup', ''))
        print(asset_info)
        #cpu = asset_info[asset_ip]['ansible_facts']['ansible_processor'][1]
        cpu = asset_info[asset_ip]['ansible_facts']['ansible_processor_vcpus']
        memory = asset_info[asset_ip]['ansible_facts']['ansible_memtotal_mb']
        disk = asset_info[asset_ip]['ansible_facts']['ansible_devices']['sda']['size']
        system_type = asset_info[asset_ip]['ansible_facts']['ansible_lsb']['id']
        system_version = asset_info[asset_ip]['ansible_facts']['ansible_lsb']['release']
        system_arch = asset_info[asset_ip]['ansible_facts']['ansible_machine']
        sn = asset_info[asset_ip]['ansible_facts']['ansible_product_serial']
        mac = asset_info[asset_ip]['ansible_facts']['ansible_default_ipv4']['macaddress']
        asset.cpu = cpu
        asset.memory = memory * 1024 * 1024
        asset.disk = disk
        asset.system_type = system_type
        asset.system_version = system_version
        asset.system_arch = system_arch
        asset.sn = sn
        asset.mac = mac
        asset.save()
        mess = 'true'
    except NameError as e:
        print(e,'NameError')
        mess = 'ansible 执行失败！'
    except KeyError as e:
        print(e,'KeyError')
        mess = 'KeyError'
    except Exception as e:
        print(e,'Exception')
        mess = '未知错误'
    return HttpResponse(mess)


def idc(request):
    return render(request, 'cmdb/idc.html')

def test(request):
    return render(request, 'test.html')

def group_list(request):
    groups = AssetGroup.objects.all()
    print(groups)
    groups_list=[]
    for group in groups:
        group_dict = {}
        group_dict["groupname"] = group.group_name
        group_dict["hostnumber"] = len([ host for host in group.host.all()])
        group_dict["comment"] = group.comment
        groups_list.append(group_dict)
    print(groups_list)
    return render(request, 'cmdb/group_list.html',{'host': groups_list})

@csrf_exempt
@login_required
def asset_add(request):
    if request.method == 'POST':
        print(request.POST)
        hostname = request.POST.get('hostname','')
        host_ip = request.POST.get('host_ip','')
        ssh_port = request.POST.get('ssh_port','')
        idc = request.POST.get('idc','')
        groups = request.POST.get('groups','')
        is_active = True if request.POST.get('status') == 'on' else False
        print(hostname,host_ip,ssh_port,idc,groups,is_active)
        if Asset.objects.filter(hostname=hostname):
            mess = u'该主机名 %s 已存在!' % hostname
        else:
            try:
                t = Asset.objects.create(hostname=hostname,ip=host_ip,port=ssh_port,idc=IDC.objects.get(id=idc),is_active=is_active)
                for groupid in groups.strip().split(' '):
                    group = AssetGroup.objects.get(id=groupid)
                    t.group.add(group)
                mess = 'Add.True'
            except Exception as e:
                print(e)
                mess = e
        return HttpResponse(mess)
    else:
        asset_group_all = AssetGroup.objects.all()
        asset_idc_all = IDC.objects.all()
        return render(request, 'cmdb/asset_add.html',{'asset_group_all': asset_group_all, 'asset_idc_all': asset_idc_all})


def group_add(request):
    hosts = Asset.objects.all()
    host_list = [  host.host_name + " - " + host.host_ip for host in hosts ]
    print(host_list)
    return render(request, 'cmdb/group_add.html',{'host': host_list})
