#!/usr/bin/env python
# coding=utf-8
__author__ = 'yuanbin'
import sys
# from zstack_cluster_api import zstack_cluster_api
from zstack_base_demo import zstack_base_api

reload(sys)
sys.setdefaultencoding('utf-8')


class zstack_l2network_api:
    def __init__(self):
        self.header = {"Content-Type": "application/json"}
        self.base = zstack_base_api()
        # self.cluster = zstack_cluster_api()
        self.UUID = self.base.UUID

    def create_l2novlan_network(self, name, zoneUuid, physicalInterface):
        '''
        {
          "org.zstack.header.network.l2.APICreateL2NoVlanNetworkMsg": {
            "type": "L2NoVlanNetwork",
            "name": "Flat-l2-2",
            "description": null,
            "zoneUuid": "4cc9847534384039b323e8d2fff4b606",
            "physicalInterface": "em2",
            "session": {
              "uuid": "f9a89f75a78943fab298a7c145c6fdf7"
            }
          }
        }
        :param name:
        :param zoneUuid:
        :param physicalInterface:
        :return:
        '''
        content = {
            "type": "L2NoVlanNetwork",
            "name": name,
            "zoneUuid": zoneUuid,
            "physicalInterface": physicalInterface,
            "description": "create L2NoVlan Network %s" % name
         }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.network.l2.APICreateL2NoVlanNetworkMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)

        print "successfully Create L2NoVlan Network %s, status %s" % (name, status)

        # 挂在L2网络到Cluster
        # self.cluster.attach_l2network_to_cluster(uuid='')
        # pass

    def delete_l2novlan_network(self, uuid):
        '''
        {
          "org.zstack.header.network.l2.APIDeleteL2NetworkMsg": {
            "uuid": "5d01b4f5ae4c4c2892462917cc2f7387",
            "session": {
              "uuid": "f9a89f75a78943fab298a7c145c6fdf7"
            }
          }
        }
        :param uuid:
        :return:
        '''
        content = {
            "uuid": uuid
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.network.l2.APIDeleteL2NetworkMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)
        print "successfully delete L2 network %s, status %s" % (uuid, status)

    # def attch_l2network_to_cluster(self, uuid, l2uuid):
    #     self.cluster.attach_l2network_to_cluster(uuid, l2uuid)

if __name__ == '__main__':
    new_zs = zstack_l2network_api()
    try:
        # session_uuid = new_zs.login()
        # new_zs.create_l2novlan_network(name='Flat-l2-4', zoneUuid='4cc9847534384039b323e8d2fff4b606', physicalInterface='em1')
        # new_zs.attch_l2network_to_cluster('f6cf5efe72924ccf90b771d32f610f19', 'c75585d91b4b4ce5a251dd3ef471302d')
        new_zs.delete_l2novlan_network(uuid='c75585d91b4b4ce5a251dd3ef471302d')
    except:
        print "执行错误！"
    new_zs.base.logout(new_zs.UUID)
