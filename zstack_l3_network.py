#!/usr/bin/env python
# coding=utf-8
__author__ = 'yuanbin'
import sys
# from zstack_cluster_api import zstack_cluster_api
from zstack_base_demo import zstack_base_api

reload(sys)
sys.setdefaultencoding('utf-8')


class zstack_l3network_api:
    def __init__(self):
        self.header = {"Content-Type": "application/json"}
        self.base = zstack_base_api()
        self.UUID = self.base.UUID

    def create_l3_network(self, name, l2NetworkUuid):
        '''
        {
          "org.zstack.header.network.l3.APICreateL3NetworkMsg": {
            "type": "L3BasicNetwork",
            "name": "Flat-l3-2",
            "description": "test",
            "l2NetworkUuid": "954157886d8f48c48c8de76d6fc589b9",
            "system": false,
            "dnsDomain": null,
            "session": {
              "uuid": "ff7c6b819b8849e1b4725ed357d3d220"
            }
          }
        }
        :param name:
        :param l2NetworkUuid:
        :param dnsDomain:
        :return:
        '''
        content = {
            # "type": "L3BasicNetwork",
            "name": name,
            "l2NetworkUuid": l2NetworkUuid,
            "description": "create L3Network %s" % name
         }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.network.l3.APICreateL3NetworkMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        response = self.base.query_until_done_other(job_uuid)

        print "successfully Create L3Network %s, status %s" % (name, 'done')
        return response['uuid']

    def add_ip_range(self, name, l3NetworkUuid, startIp, endIp, gateway, netmask):
        '''
        {
          "org.zstack.header.network.l3.APIAddIpRangeMsg": {
            "l3NetworkUuid": "ddf818186ce243aa8d026f132e3f406d",
            "startIp": "10.0.1.11",
            "endIp": "10.0.1.20",
            "gateway": "10.0.1.1",
            "netmask": "255.255.255.0",
            "name": "ipr-range",
            "description": null,
            "session": {
              "uuid": "ff7c6b819b8849e1b4725ed357d3d220"
            }
          }
        }
        :return:
        '''

        content = {
            "type": "L3BasicNetwork",
            "name": name,
            "l3NetworkUuid": l3NetworkUuid,
            "startIp": startIp,
            "endIp": endIp,
            "gateway": gateway,
            "netmask": netmask,
            "description": "Add Ip Ranges %s,from %s to %s" % (name, startIp, endIp)
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.network.l3.APIAddIpRangeMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)

        print "successfully Add Ip Ranges for L3Network %s, status %s" % (name, status)

    def add_dns_to_l3network(self, dns, l3NetworkUuid):
        '''
        {
          "org.zstack.header.network.l3.APIAddDnsToL3NetworkMsg": {
            "dns": "8.8.8.8",
            "l3NetworkUuid": "ddf818186ce243aa8d026f132e3f406d",
            "session": {
              "uuid": "ff7c6b819b8849e1b4725ed357d3d220"
            }
          }
        }
        :return:
        '''

        content = {
            "dns": dns,
            "l3NetworkUuid": l3NetworkUuid
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.network.l3.APIAddDnsToL3NetworkMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)

        print "successfully Add DNS %s to L3Network, status %s" % (dns, status)


    def attach_networkservice_to_l3network(self, l3NetworkUuid):
        '''
        {
          "org.zstack.header.network.service.APIAttachNetworkServiceToL3NetworkMsg": {
            "l3NetworkUuid": "ddf818186ce243aa8d026f132e3f406d",
            "networkServices": {
              "34e444dabc4e421faf59275bbb598d2f": [
                "DHCP",
                "Userdata"
              ]
            },
            "session": {
              "uuid": "ff7c6b819b8849e1b4725ed357d3d220"
            }
          }
        }
        :return:
        '''

        content = {
            "l3NetworkUuid": l3NetworkUuid,
            "networkServices": {
                "34e444dabc4e421faf59275bbb598d2f": [
                    "DHCP",
                    "Userdata"
                ]
            }
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.network.service.APIAttachNetworkServiceToL3NetworkMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)

        print "successfully Attach NetworkService %s To L3NetworkMsg, status %s" % ("DHCP,Userdata", status)

    def delete_l3network(self, uuid):
        '''
        {
          "org.zstack.header.network.l3.APIDeleteL3NetworkMsg": {
            "uuid": "22f5d39b88894b83acecb8e950322829",
            "session": {
              "uuid": "afc9c711bb7242d69caa292633f7d3b2"
            }
          }
        }'''
        content = {
            "uuid": uuid
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.network.l3.APIDeleteL3NetworkMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)
        print "successfully delete L3 network %s, status %s" % (uuid, status)

    # def attch_l2network_to_cluster(self, uuid, l2uuid):
    #     self.cluster.attach_l2network_to_cluster(uuid, l2uuid)

if __name__ == '__main__':
    new_zs = zstack_l3network_api()
    try:
        # session_uuid = new_zs.login()
        # new_zs.create_l3_network('Flat-l3-3', 'b0e9204d44a844ed837667b57181a8bd')
        # new_zs.add_ip_range('test-ranges', '81a2a22fce3149bfaea2a5c7354095c2', '10.0.2.130', '10.0.2.140', '10.0.2.1', '255.255.255.0')
        # new_zs.add_dns_to_l3network('114.114.114.114', '81a2a22fce3149bfaea2a5c7354095c2')
        new_zs.attach_networkservice_to_l3network('81a2a22fce3149bfaea2a5c7354095c2')
    except:
        print "执行错误！"
    new_zs.base.logout(new_zs.UUID)
