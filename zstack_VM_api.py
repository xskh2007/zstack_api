#!/usr/bin/env python
# coding=utf-8
__author__ = 'yuanbin'
import sys
from zstack_base_demo import zstack_base_api

reload(sys)
sys.setdefaultencoding('utf-8')


class zstack_vminstance_api:
    def __init__(self):
        self.header = {"Content-Type": "application/json"}
        self.base = zstack_base_api()
        self.UUID = self.base.UUID
        # pass

    def create_vminstance(self, name, instanceOfferingUuid, imageUuid, l3NetworkUuids, hostUuid, clusterUuid, zoneUuid):
        '''
        {
          "org.zstack.header.vm.APICreateVmInstanceMsg": {
            "name": "vm-6xav",
            "description": null,
            "instanceOfferingUuid": "545a4cc398064c469ed498f5bd392c95",
            "imageUuid": "ac57e254210e479b9050dc6c1cc10e8d",
            "l3NetworkUuids": [
              "235ee7cfc64e4fd1a2aa1ad8f55cba03"
            ],
            "rootDiskOfferingUuid": "609ef21cfac44c50af6407bf02f22d07",
            "dataDiskOfferingUuids": [],
            "zoneUuid": "4cc9847534384039b323e8d2fff4b606",
            "clusterUuid": "f6cf5efe72924ccf90b771d32f610f19",
            "hostUuid": "f3e90e2620f840618a8941b6688101b9",
            "resourceUuid": "b5d71800ae9d40d288d7e85734c1742d",
            "defaultL3NetworkUuid": "235ee7cfc64e4fd1a2aa1ad8f55cba03",
            "systemTags": [],
            "session": {
              "uuid": "545b63ed13794ab8abb43c2e4a922a2f"
            }
          }
        }
        :param name: 云主机的名称
        :param instanceOfferingUuid: CPU和内存
        :param imageUuid: 镜像
        :param l3NetworkUuids: 3层网络
        :param hostUuid: 物理宿主机
        :param clusterUuid: 集群
        :param zoneUuid: 区域
        :return:
        '''
        content = {
            "name": name,
            "instanceOfferingUuid": instanceOfferingUuid,
            "imageUuid": imageUuid,
            "l3NetworkUuids": [l3NetworkUuids],
            "hostUuid": hostUuid,
            "clusterUuid": clusterUuid,
            "zoneUuid": zoneUuid,
            "description": "create vm instance %s" % name
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.vm.APICreateVmInstanceMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)

        print "successfully Create VmInstance %s, status %s" % (name, status)
        # pass

    def delete_vminstance(self, uuid):
        '''
        {
          "org.zstack.header.vm.APIDestroyVmInstanceMsg": {
            "uuid": "b5d71800ae9d40d288d7e85734c1742d",
            "session": {
              "uuid": "92c728dc54ab42bf9f61d4b6664a3133"
            }
          }
        }
        :param uuid: 云主机的uuid
        :return:
        '''
        content = {
            "uuid": uuid
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.vm.APIDestroyVmInstanceMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)
        print "successfully delete VM Instance %s, status %s" % (uuid, status)

    def start_vminstance(self, uuid):
        '''
        {
          "org.zstack.header.vm.APIStartVmInstanceMsg": {
            "uuid": "bbb9878551e64267b46d3b1bdaddd2b9",
            "session": {
              "uuid": "92c728dc54ab42bf9f61d4b6664a3133"
            }
          }
        }
        :param uuid:
        :return:
        '''
        content = {
            "uuid": uuid
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.vm.APIStartVmInstanceMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)
        print "successfully Start VM Instance %s, status %s" % (uuid, status)

    def stop_vminstance(self, uuid):
        '''
        {
          "org.zstack.header.vm.APIStopVmInstanceMsg": {
            "uuid": "bbb9878551e64267b46d3b1bdaddd2b9",
            "session": {
              "uuid": "92c728dc54ab42bf9f61d4b6664a3133"
            }
          }
        }
        :param uuid:
        :return:
        '''
        content = {
            "uuid": uuid
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.vm.APIStopVmInstanceMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)
        print "successfully Stop VM Instance %s, status %s" % (uuid, status)

    def reboot_vminstance(self, uuid):
        '''
        {
          "org.zstack.header.vm.APIRebootVmInstanceMsg": {
            "uuid": "cf77007ab67d4b1fade3c9363c3deadd",
            "session": {
              "uuid": "92c728dc54ab42bf9f61d4b6664a3133"
            }
          }
        }
        :param uuid:
        :return:
        '''
        content = {
            "uuid": uuid
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.vm.APIRebootVmInstanceMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.base.query_until_done(job_uuid)
        print "successfully Reboot VM Instance %s, status %s" % (uuid, status)

    def migrate_vm(self, uuid):
        pass

    def query_vm_nic_by_ip(self, ip):
        '''
        {
            "org.zstack.header.vm.APIQueryVmNicMsg": {
                "session": {
                    "uuid": "765c6b5436d146ef9bc283ddaa81fbee"
                    },
                "conditions": [
                    {
                        "name": "ip",
                        "value": "10.0.1.2",
                        "op": "="
                    }
                ]
            }
        }
        :param uuid:
        :return:
        '''
        content = {
            "conditions": [
                {
                    "name": "ip",
                    "value": ip,
                    "op": "="
                }
            ]
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.vm.APIQueryVmNicMsg", content)
        self.base.error_if_fail(rsp)

        print "successfully query NIC from VMInstance %s, result: %s" % (ip, rsp)
        return rsp

    def query_vm_volume_by_vminstanceuuid(self, vminstanceuuid):
        '''
        {
            "org.zstack.header.volume.APIQueryVolumeMsg": {
                "session": {"uuid": "8cc578e62d814ffa98bb9d89c8b5398a"},
                "conditions": [{"name": "vmInstanceUuid", "value": "74f6bc08e7ba431a8ac858a4fd7caaff", "op": "="}]
            }
        }
        :param uuid:
        :return:
        '''
        content = {
            "conditions": [
                {
                    "name": "vmInstanceUuid",
                    "value": vminstanceuuid,
                    "op": "="
                }
            ]
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.volume.APIQueryVolumeMsg", content)

        # print "successfully Query VM Instance NIC %s, status %s" % (uuid, status)
        self.base.error_if_fail(rsp)

        print "successfully query Volume from VMInstance uuid %s, result: %s" % (vminstanceuuid, rsp)
        return rsp

    def query_vm(self, hostUuid, limit):
        '''
        {
            "org.zstack.header.vm.APIQueryVmInstanceMsg": {
                "conditions": [{"name": "hostUuid", "value": "f3e90e2620f840618a8941b6688101b9", "op": "="}],
                "session": {"uuid": "8cc578e62d814ffa98bb9d89c8b5398a"},
                "limit": "10"
            }
        }
        :param hostUuid:clusterUuid:rootVolumeUuid
        :param state:uuid:zoneUuid
        :param name:platform:instanceOfferingUuid
        :param limit:
        :return:
        '''
        content = {
            "conditions": [
                {
                    "name": "hostUuid",
                    "value": hostUuid,
                    "op": "="
                }
            ],
            "limit": limit
        }

        rsp = self.base.api_call(self.UUID, "org.zstack.header.vm.APIQueryVmInstanceMsg", content)

        # print "successfully Query VM Instance NIC %s, status %s" % (uuid, status)
        self.base.error_if_fail(rsp)

        print "successfully query VMInstance from hostUuid %s, result: %s" % (hostUuid, rsp)
        return rsp

if __name__ == '__main__':
    new_zs = zstack_vminstance_api()
    try:
        # session_uuid = new_zs.login()
        # new_zs.create_vminstance(name='flat-vm-4', instanceOfferingUuid='545a4cc398064c469ed498f5bd392c95',
        #                          l3NetworkUuids='845171a140a64af692fd9d18ee53f06c',
        #                          imageUuid='ac57e254210e479b9050dc6c1cc10e8d',
        #                          hostUuid='f3e90e2620f840618a8941b6688101b9',
        #                          clusterUuid='f6cf5efe72924ccf90b771d32f610f19',
        #                          zoneUuid='4cc9847534384039b323e8d2fff4b606')
        # new_zs.delete_vminstance(uuid='c24e18d9403a41d8b67d588137c97d55')
        new_zs.query_vm_nic_by_ip(ip='10.0.10.88')
        # new_zs.query_vm_volume_by_vminstanceuuid(vminstanceuuid='a4312e5eee944367ab74a27e4e805800')
        # new_zs.stop_vminstance('aa83dbbc5d9c415095c1a3b6681d0211')
        # new_zs.start_vminstance('aa83dbbc5d9c415095c1a3b6681d0211')
        # new_zs.query_vm('f3e90e2620f840618a8941b6688101b9', 3)
        # new_zs.logout(new_zs.UUID)
    except Exception, e:
        print "执行错误！", e

    new_zs.base.logout(new_zs.UUID)
