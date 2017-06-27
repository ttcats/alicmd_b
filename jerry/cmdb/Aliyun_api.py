#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import SetLoadBalancerNameRequest, AddBackendServersRequest, RemoveBackendServersRequest, DescribeLoadBalancersRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceTypesRequest, DescribeDisksRequest
import json


class Aliyunapi(object):
    def __init__(self):
        self.clt = client.AcsClient(
            'xxxxxxxxxxxx',
            'xxxxxxxxxxxxxxxxxxxxxxxxxx',
            'cn-hangzhou')

    def request_api(self, request, *values):
        if values:
            for value in values:
                for k, v in value.iteritems():
                    request.add_query_param(k, v)
        request.set_accept_format('xml')
        result = self.clt.do_action_with_exception(request)
        return json.loads(result)

    def describeloadbalancer(self, loadbalancername):
        '''查询slb信息'''
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        values = {"RegionId": "cn-hangzhou",
                  "LoadBalancerName": str(loadbalancername)}
        info = self.request_api(request, values)[
            'LoadBalancers']['LoadBalancer']
        if info:
            return [loadbalancer_info['LoadBalancerId']
                    for loadbalancer_info in info]

    def describedisks(self, instanceid=None):
        '''查询磁盘'''
        page = 0
        disks_info = []
        while True:
            page += 1
            values = {"RegionId": "cn-hangzhou", "PageNumber": page, "PageSize": 100}
            if instanceid:
                values = {"RegionId": "cn-hangzhou", "InstanceId": instanceid}
            request = DescribeDisksRequest.DescribeDisksRequest()
            #info = self.request_api(request, values)['Disks']['Disk']
            info = self.request_api(request, values)
            for disk_info in info['Disks']['Disk']:
                if disk_info['Category'] == 'cloud_efficiency':
                    disk_info['Category'] = 'efficiency'
                if disk_info['Category'] == 'cloud_ssd':
                    disk_info['Category'] = 'ssd'
                disks_info.append({disk_info['InstanceId']:[disk_info['Size'],disk_info['Category']]})
            if len(info['Disks']['Disk']) != 100:
                break
        return disks_info

    def describeinstancetypes(self, instancetypefamily=None):
        '''查询 ECS 所提供的实例资源规格CPU/Mem'''
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        values = {"Action": "DescribeInstanceTypes"}
        if instancetypefamily:
            values = {"Action": "DescribeInstanceTypes","InstanceTypeFamily": instancetypefamily}
        info = self.request_api(request, values)['InstanceTypes']['InstanceType']
        ecs_types = []
        for ecs_type in info:
            ecs_types.append({ecs_type['InstanceTypeId']:[ecs_type['CpuCoreCount'],ecs_type['MemorySize']]})
        return ecs_types


    def describeinstance(self, ecsip=None):
        '''查询ecs信息'''
        page = 0
        ecs_instanceids = []
        while True:
            page += 1
            values = {"RegionId": "cn-hangzhou", "PageNumber": page, "PageSize": 100}
            if ecsip:
                values = {"RegionId": "cn-hangzhou", "InnerIpAddresses": [str(ecsip)], "PageNumber": page, "PageSize": 100}
            request = DescribeInstancesRequest.DescribeInstancesRequest()
            Instances_info = self.request_api(request, values)
            for ecs_info in Instances_info['Instances']['Instance']:
                #ecs_instanceids.append({ecs_info['InstanceId']:[ecs_info['InstanceName'],ecs_info['InnerIpAddress']]})
                ecs_instanceids.append({ecs_info['InstanceId']:[{'InstanceName':ecs_info['InstanceName']},{'Memory':ecs_info['Memory']},{'Cpu':ecs_info['Cpu']},{'OSName':ecs_info['OSName']},ecs_info['PublicIpAddress'],ecs_info['InnerIpAddress'],{'Status':ecs_info['Status']},{'ExpiredTime':ecs_info['ExpiredTime']}]})
            if len(Instances_info['Instances']['Instance']) != 100:
                break
        return ecs_instanceids


    def addbackendserver(self, loadbalancername, serverip):
        '''添加后端ecs服务器'''
        loadbalancerids = self.describeloadbalancer(loadbalancername)
        serverid = self.describeinstance(serverip)
        if not loadbalancerids or not serverid:
            print('slb or server is not found!')
        else:
            for loadbalancerid in loadbalancerids:
                request = AddBackendServersRequest.AddBackendServersRequest()
                values = {"LoadBalancerId": str(loadbalancerid), "BackendServers": [
                    {'ServerId': str(serverid[0]), 'Weight':'100'}]}
                mess = self.request_api(request, values)['BackendServers']
                print(mess)

    def removebackendserver(self, loadbalancername, serverip):
        '''删除后端ecs服务器'''
        loadbalancerids = self.describeloadbalancer(loadbalancername)
        serverid = self.describeinstance(serverip)
        if not loadbalancerids or not serverid:
            print('slb or server is not found!')
        else:
            for loadbalancerid in loadbalancerids:
                request = RemoveBackendServersRequest.RemoveBackendServersRequest()
                values = {"LoadBalancerId": str(loadbalancerid), "BackendServers": [
                    str(serverid[0])]}
                mess = self.request_api(request, values)['BackendServers']
                print(mess)

    def setLoadbalancername(self, loadbalancername, newloadbalancername):
        '''更改slb的别名'''
        loadbalancerids = self.describeloadbalancer(loadbalancername)
        if loadbalancerids and len(loadbalancerids) == 1:
            request = SetLoadBalancerNameRequest.SetLoadBalancerNameRequest()
            values = {
                "LoadBalancerId": str(
                    loadbalancerids[0]),
                "LoadBalancerName": newloadbalancername}
            mess = self.request_api(request, values)
            print(mess)
        else:
            print('no loadbalancer or loadbalancername is not the only one!')


if __name__ == '__main__':
    t = Aliyunapi()
    #print(t.describeinstance('10.27.232.144'))
    print(t.describeinstance())
    #print(t.describeinstancetypes())
    #print(t.describedisks('i-23tz68972'))
    #print(t.describedisks())
    #t.addbackendserver('user-app-lan1', '10.7.2.5')
    #t.removebackendserver('user-app-lan1', '10.7.2.5')
    #t.setLoadbalancername('user-app-lan1', 'user-app-lan4')
