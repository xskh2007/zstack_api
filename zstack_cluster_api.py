#!/usr/bin/env python
#coding=utf-8
__author__ = 'yuanbin'
import sys
import os
import config
import time
import requests
import json

reload(sys)
sys.setdefaultencoding('utf-8')

class zstack_cluster_api:
    def __init__(self):
        self.header = {"Content-Type": "application/json"}
        self.url = config.URL
        self.url_result = config.URL_RESULT
        self.name = config.NAME
        self.password = config.PASSWORD

        self.UUID = self.login()
        # pass

    def query_until_done(self, job_uuid):
        # conn.request("GET", "/zstack/api/result/%s" % job_uuid)
        request = requests.get(self.url_result + str(job_uuid))

        response = json.loads(request.content)
        # rsp = json.loads(rsp_body)
        if response["state"] == "Done":
            return response["state"]

        time.sleep(1)
        print "Job[uuid:%s] is still in processing" % job_uuid
        return self.query_until_done(job_uuid)

    def api_call(self, session_uuid, api_id, api_content):
        if session_uuid:
            api_content["session"] = {"uuid": session_uuid}
        api_body = {api_id: api_content}

        request = requests.post(self.url, data=json.dumps(api_body), headers=self.header)
        response = json.loads(request.content)
        if "result" in response.keys():
            result = json.loads(response['result'])
        else:
            result = response
        return result

    def error_if_fail(self, rsp):
        success = rsp.values()[0]["success"]
        if not success:
            error = rsp.values()[0]["error"]
            raise Exception("failed to login, %s" % json.dumps(error))

    def login(self):
        content = {
            "accountName": self.name,
            "password": self.password
        }

        rsp = self.api_call(None, "org.zstack.header.identity.APILogInByAccountMsg", content)
        self.error_if_fail(rsp)

        session_uuid = rsp.values()[0]["inventory"]["uuid"]

        print "successfully login, session uuid is: %s" % session_uuid
        return session_uuid


    """
    zoneUuid        父区域的uuid
    name            资源名称
    resourceUuid    资源uuid
    description     资源描述
    hypervisorType  虚拟机管理类型，zstack仅支持KVM
    type            保留域，不要使用
    """
    def create_cluster(self, name='cluster-default', zoneUuid=""):
        '''request:{
                "org.zstack.header.cluster.APICreateClusterMsg":
                    {
                        "session": {"uuid": "e360e25b28cb49eca00ea9117e23018b"},
                        "zoneUuid": "46627d3eafb9462dbafa35c96d9db302",
                        "hypervisorType": "KVM",
                        "name": "cluster-look"
                    }
            }
            response: {
                "org.zstack.header.cluster.APICreateClusterEvent":
                    {
                        "inventory":
                            {
                                "name":"cluster-look",
                                "uuid":"73a5d13f020d450e997f2aa04350ac3c",
                                "state":"Enabled",
                                "hypervisorType":"KVM",
                                "createDate":"Sep 27, 2016 10:10:40 PM",
                                "lastOpDate":"Sep 27, 2016 10:10:40 PM",
                                "zoneUuid":"46627d3eafb9462dbafa35c96d9db302",
                                "type":"zstack"
                            },
                        "success":true
                    }
            }'''
        if len(zoneUuid) == 0:
            print "zoneUuid is null, can not continue to create cluster."
            return {}
        content = {
            "name": name,
            "hypervisorType": "KVM",
            "zoneUuid": zoneUuid,
            # "resourceUuid": resourceUuid,
            "description": "with ops, auto create " + name,
            # "type": type
        }

        rsp = self.api_call(self.UUID, "org.zstack.header.cluster.APICreateClusterMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully created %s, status %s" % (name, status)
        # pass

    def delete_cluster(self, uuid):
        '''
        request: {
            "org.zstack.header.cluster.APIDeleteClusterMsg":
                {
                    "session": {"uuid": "b1de35faa6eb4c4298dd92b89119516e"},
                    "uuid": "1e3aedbc71d44d1cafa5ff123c988cb5"
                }
        }
        response: {
            "org.zstack.header.cluster.APIDeleteClusterEvent":
                {"success":true}
        }
        :param uuid: Cluster UUID
        :return:
        '''
        content = {"uuid": uuid}

        rsp = self.api_call(self.UUID, "org.zstack.header.cluster.APIDeleteClusterMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully delete %s, status %s" % (uuid, status)

        # return self.UUID
        # pass

    def change_cluster_state(self, uuid, stateEvent):
        '''
        request: {
            "org.zstack.header.cluster.APIChangeClusterStateMsg":
                {
                    "session": {"uuid": "b1de35faa6eb4c4298dd92b89119516e"},
                    "uuid": "73a5d13f020d450e997f2aa04350ac3c",
                    "stateEvent": "disable"
                }
        }
        response: {
            "org.zstack.header.cluster.APIChangeClusterStateEvent":
                {
                    "inventory":
                        {
                            "name":"cluster-look",
                            "uuid":"73a5d13f020d450e997f2aa04350ac3c",
                            "state":"Disabled",
                            "hypervisorType":"KVM",
                            "createDate":"Sep 27, 2016 10:10:40 PM",
                            "lastOpDate":"Sep 27, 2016 11:08:43 PM",
                            "zoneUuid":"46627d3eafb9462dbafa35c96d9db302",
                            "type":"zstack"
                        },
                    "success":true
                }
        }
        :param uuid: 集群的uuid
        :param stateEvent: enable/disable
        :return:
        '''
        content = {
            "uuid": uuid,
            "stateEvent": stateEvent
        }

        rsp = self.api_call(self.UUID, "org.zstack.header.cluster.APIChangeClusterStateMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully change cluster state %s, status %s" % (uuid, status)

    def attach_primary_storage_to_cluster(self, uuid, psuuid):
        '''
        request: {
            "org.zstack.header.storage.primary.APIAttachPrimaryStorageToClusterMsg":
                {
                    "primaryStorageUuid": "8438a03dc6e04be38dae8d56207508b2",
                    "session": {"uuid": "b1de35faa6eb4c4298dd92b89119516e"},
                    "clusterUuid": "f6cf5efe72924ccf90b771d32f610f19"
                }
        }
        response: {
            "org.zstack.header.storage.primary.APIAttachPrimaryStorageToClusterEvent":
                {
                "inventory":
                    {
                        "uuid":"8438a03dc6e04be38dae8d56207508b2",
                        "zoneUuid":"4cc9847534384039b323e8d2fff4b606",
                        "name":"Primary_Storage-1",
                        "url":"/data",
                        "description":"???01 - 10.0.1.221 ????",
                        "totalCapacity":11998530109440,
                        "availableCapacity":11998530109440,
                        "totalPhysicalCapacity":11998530109440,
                        "availablePhysicalCapacity":11940231933952,
                        "systemUsedCapacity":58298175488,
                        "type":"LocalStorage",
                        "state":"Enabled",
                        "status":"Connected",
                        "mountPath":"/data",
                        "createDate":"Sep 26, 2016 11:28:56 AM",
                        "lastOpDate":"Sep 27, 2016 10:37:10 PM",
                        "attachedClusterUuids":["f6cf5efe72924ccf90b771d32f610f19"]
                    },
                "success":true
            }
        }
        :param uuid: 集群(Cluster)的uuid
        :param psuuid: 主存储(Primary Storage)的uuid
        :return:
        '''
        content = {
            "clusterUuid": uuid,
            "primaryStorageUuid": psuuid
        }

        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIAttachPrimaryStorageToClusterMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully Attach Primary Sstorage %s, status %s" % (uuid, status)

    def detach_primary_storage_from_cluster(self, uuid, psuuid):
        '''

        :param uuid: 集群(Cluster)的uuid
        :param psuuid: 主存储(Primary Storage)的uuid
        :return:
        '''
        content = {
            "clusterUuid": uuid,
            "primaryStorageUuid": psuuid
        }

        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIDetachPrimaryStorageFromClusterMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully Detach Primary Storage %s, status %s" % (uuid, status)

    def attach_l2network_to_cluster(self, uuid, l2uuid):
        content = {
            "clusterUuid": uuid,
            "l2NetworkUuid": l2uuid
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.network.primary.APIAttachL2NetworkToClusterMsg",
                            content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully Attach L2Network To Cluster %s, status %s" % (uuid, status)
        # pass

    def detach_l2network_from_cluster(self, uuid, l2uuid):
        content = {
            "clusterUuid": uuid,
            "l2NetworkUuid": l2uuid
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.network.primary.APIDetachL2NetworkFromClusterMsg",
                            content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully Detach L2Network From Cluster %s, status %s" % (uuid, status)
        # pass

    def query_cluster_by_clusteruuid(self, clusterUuid):
        '''
        request: {
            "org.zstack.header.cluster.APIQueryClusterMsg":
                {
                    "session":{"uuid": "68b7f784500640feac28c09c2015a0b4"},
                    "conditions": [{"name": "uuid", "value": "f6cf5efe72924ccf90b771d32f610f19", "op": "="}]
                }
        }
        response: {
            "org.zstack.header.cluster.APIQueryClusterReply":
                {
                    "inventories":
                    [
                        {
                            "name":"cluster-zb01",
                            "uuid":"f6cf5efe72924ccf90b771d32f610f19",
                            "description":"?????",
                            "state":"Enabled",
                            "hypervisorType":"KVM",
                            "createDate":"Sep 26, 2016 11:25:28 AM",
                            "lastOpDate":"Sep 27, 2016 11:16:25 PM",
                            "zoneUuid":"4cc9847534384039b323e8d2fff4b606",
                            "type":"zstack"
                        }
                    ],
                    "success":true
                }
        }
        :param clusterUuid:
        :return:
        '''

        content = {
            "conditions": [
                {
                    "name": "uuid",
                    "value": clusterUuid,
                    "op": "="
                }
            ]
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.cluster.APIQueryClusterMsg",
                            content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)
        print "successfully Query Cluster by cluster uuid %s" % (clusterUuid)

        print rsp

    def query_cluster_by_clustername(self, clusterName):
        '''
        request: {
            "org.zstack.header.cluster.APIQueryClusterMsg":
                {
                    "session":{"uuid": "68b7f784500640feac28c09c2015a0b4"},
                    "conditions": [{"name": "name", "value": "cluster-zb", "op": "="}]
                }
        }
        response: {
            "org.zstack.header.cluster.APIQueryClusterReply":
                {
                    "inventories":
                    [
                        {
                            "name":"cluster-zb01",
                            "uuid":"f6cf5efe72924ccf90b771d32f610f19",
                            "description":"?????",
                            "state":"Enabled",
                            "hypervisorType":"KVM",
                            "createDate":"Sep 26, 2016 11:25:28 AM",
                            "lastOpDate":"Sep 27, 2016 11:16:25 PM",
                            "zoneUuid":"4cc9847534384039b323e8d2fff4b606",
                            "type":"zstack"
                        }
                    ],
                    "success":true
                }
        }
        :param clusterUuid:
        :return:
        '''

        content = {
            "conditions": [
                {
                    "name": "name",
                    "value": clusterName,
                    "op": "="
                }
            ]
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.cluster.APIQueryClusterMsg",content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)
        print "successfully Query Cluster by cluster name %s" % (clusterName)
        print rsp

    def query_cluster_by_zoneuuid(self, zoneUuid):
        '''
        request: {
            "org.zstack.header.cluster.APIQueryClusterMsg":
                {
                    "session":{"uuid": "68b7f784500640feac28c09c2015a0b4"},
                    "conditions": [{"name": "zoneUuid", "value": "4cc9847534384039b323e8d2fff4b606", "op": "="}]
                }
        }
        response: {
            "org.zstack.header.cluster.APIQueryClusterReply":
                {
                    "inventories":
                    [
                        {
                            "name":"cluster-zb01",
                            "uuid":"f6cf5efe72924ccf90b771d32f610f19",
                            "description":"?????",
                            "state":"Enabled",
                            "hypervisorType":"KVM",
                            "createDate":"Sep 26, 2016 11:25:28 AM",
                            "lastOpDate":"Sep 27, 2016 11:16:25 PM",
                            "zoneUuid":"4cc9847534384039b323e8d2fff4b606",
                            "type":"zstack"
                        }
                    ],
                    "success":true
                }
        }
        :param clusterUuid:
        :return:
        '''

        content = {
            "conditions": [
                {
                    "name": "zoneUuid",
                    "value": zoneUuid,
                    "op": "="
                }
            ]
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.cluster.APIQueryClusterMsg",
                            content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)
        print "successfully Query Cluster by zone uuid %s" % (zoneUuid)
        print rsp

    def logout(self, session_uuid):
        content = {"sessionUuid": session_uuid}
        rsp = self.api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
        self.error_if_fail(rsp)

        print "successfully logout"
        # pass


if __name__ == '__main__':
    new_zs = zstack_cluster_api()
    # session_uuid = new_zs.login()
    new_zs.create_cluster('cluster-yu', 'c9df649b419243b597b1dec99b90833f')
    # new_zs.delete_cluster('6c965d8775f440efa18471dec8e3b12a')
    # new_zs.change_cluster_state('f6cf5efe72924ccf90b771d32f610f19', 'enable')
    # new_zs.attach_primary_storage_to_cluster('f6cf5efe72924ccf90b771d32f610f19', '8438a03dc6e04be38dae8d56207508b2')
    # new_zs.detach_primary_storage_from_cluster('f6cf5efe72924ccf90b771d32f610f19', '8438a03dc6e04be38dae8d56207508b2')
    # zone_list = new_zs.query_cluster_by_clustername('cluster-zb01')
    # zone_list = new_zs.query_cluster_by_clusteruuid('f6cf5efe72924ccf90b771d32f610f19')

    new_zs.logout(new_zs.UUID)