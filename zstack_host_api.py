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

class zstack_host_api:
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

    def add_kvm_host(self, name, clusterUuid, managementIp, username, password):
        '''
        request: {
            "org.zstack.kvm.APIAddKVMHostMsg":
                {
                    "username": "root",
                    "clusterUuid": "f6cf5efe72924ccf90b771d32f610f19",
                    "name": "host-yuan",
                    "managementIp": "10.0.3.119",
                    "session": {"uuid": "0962b18d361446788a635b9b904d8711"},
                    "password": "Skt6edg"
                }
        }
        :param name:
        :param clusterUuid:
        :param managementIp:
        :param username:
        :param password:
        :return:
        '''
        content = {
            "name": name,
            "clusterUuid": clusterUuid,
            "managementIp": managementIp,
            "username": username,
            "password": password,
            "description": "Add KVM Host: %s" % name
        }

        rsp = self.api_call(self.UUID, "org.zstack.kvm.APIAddKVMHostMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully created %s, status %s" % (name, status)
        # pass

    def delete_host(self, uuid):
        '''
        request: {
            "org.zstack.header.host.APIDeleteHostMsg": {
                "session": {"uuid": "0962b18d361446788a635b9b904d8711"},
                "uuid": "848520f29011436c8685e520b87dab23"
            }
        }
        :param uuid:
        :return:
        '''
        content = {"uuid": uuid}

        rsp = self.api_call(self.UUID, "org.zstack.header.host.APIDeleteHostMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully delete Host %s, status %s" % (uuid, status)

        # return self.UUID
        # pass

    def change_host_state(self, uuid, stateEvent):
        '''
        request: {
            "org.zstack.header.host.APIChangeHostStateMsg":
                {
                    "session": {"uuid": "0962b18d361446788a635b9b904d8711"},
                    "uuid": "848520f29011436c8685e520b87dab23",
                    "stateEvent": "disable"
                }
        }
        response: {
            "org.zstack.header.host.APIChangeHostStateEvent":
                {
                    "inventory":
                        {
                            "zoneUuid":"4cc9847534384039b323e8d2fff4b606",
                            "name":"host-yb",
                            "uuid":"848520f29011436c8685e520b87dab23",
                            "clusterUuid":"aac8b6ea037044b389b2849090fa9bb6",
                            "description":"Add KVM Host: host-yb",
                            "managementIp":"10.0.89.18",
                            "hypervisorType":"KVM",
                            "state":"Disabled",
                            "status":"Connected",
                            "totalCpuCapacity":40,
                            "availableCpuCapacity":40,
                            "totalMemoryCapacity":8071839744,
                            "availableMemoryCapacity":8071839744,"
                            createDate":"Sep 28, 2016 4:22:42 AM",
                            "lastOpDate":"Sep 28, 2016 4:31:43 AM"
                        },
                    "success":true
                }
        }
        :param uuid: 主机的uuid
        :param stateEvent: enable/disable/preMaintain
        :return:
        '''
        content = {
            "uuid": uuid,
            "stateEvent": stateEvent
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.host.APIChangeHostStateMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully Change Host State %s, status %s" % (uuid, status)
        # pass

    def reconnect_host(self, uuid):
        '''
        request: {
            "org.zstack.header.host.APIReconnectHostMsg":{
                "session": {"uuid": "0962b18d361446788a635b9b904d8711"},
                "uuid": "848520f29011436c8685e520b87dab23"
            }
        }
        response: {
            "org.zstack.header.host.APIReconnectHostEvent":{
                "success":true
            }
        }
        :param uuid: 主机的uuid
        :return:
        '''
        content = {
            "uuid": uuid
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.host.APIChangeHostStateMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully Reconnect Host %s, status %s" % (uuid, status)
        # pass

    def query_host_by_ip(self, managementIP):
        '''
        request: {
            "org.zstack.header.host.APIQueryHostMsg": {
                "session": {"uuid": "0962b18d361446788a635b9b904d8711"},
                "conditions": [{"name": "managementIp", "value": "10.0.89.18", "op": "="}]
            }
        }
        :param managementIP:
        :return:
        '''
        content = {
            "conditions": [
                {
                    "name": "managementIp",
                    "value": managementIP,
                    "op": "="
                }
            ]
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.host.APIQueryHostMsg", content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)

        print "successfully query Host by managementIP %s, result: %s" % (managementIP, rsp)
        # pass

    def query_host_by_name(self, name):
        '''
            request: {
                "org.zstack.header.host.APIQueryHostMsg": {
                    "session": {"uuid": "0962b18d361446788a635b9b904d8711"},
                    "conditions": [{"name": "name", "value": "host-yb", "op": "="}]
                }
            }
            :param name: Host 名称NAME
            :return:
            '''
        content = {
            "conditions": [
                {
                    "name": "name",
                    "value": name,
                    "op": "="
                }
            ]
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.host.APIQueryHostMsg", content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)

        print "successfully query Host by name %s, result: %s" % (name, rsp)

    def query_all_host(self):
        '''
        # 查询全部Host，conditions不需要过滤任何条件
        request: {
            "org.zstack.header.host.APIQueryHostMsg": {
                "session": {"uuid": "0962b18d361446788a635b9b904d8711"},
                "conditions": []
            }
        }
        response: {
            "org.zstack.header.host.APIQueryHostReply":{
                "inventories":[
                    {
                        "username":"root",
                        "sshPort":22,
                        "zoneUuid":"4cc9847534384039b323e8d2fff4b606",
                        "name":"host-yb",
                        "uuid":"848520f29011436c8685e520b87dab23",
                        "clusterUuid":"aac8b6ea037044b389b2849090fa9bb6",
                        "description":"Add KVM Host: host-yb",
                        "managementIp":"10.0.89.18",
                        "hypervisorType":"KVM",
                        "state":"Enabled",
                        "status":"Connected",
                        "totalCpuCapacity":40,
                        "availableCpuCapacity":40,
                        "totalMemoryCapacity":8071839744,
                        "availableMemoryCapacity":8071839744,
                        "createDate":"Sep 28, 2016 4:22:42 AM",
                        "lastOpDate":"Sep 28, 2016 4:42:28 AM"
                    },
                    {
                        "username":"root",
                        "sshPort":22,
                        "zoneUuid":"4cc9847534384039b323e8d2fff4b606",
                        "name":"host-221",
                        "uuid":"f3e90e2620f840618a8941b6688101b9",
                        "clusterUuid":"f6cf5efe72924ccf90b771d32f610f19",
                        "description":"10.0.1.221",
                        "managementIp":"10.0.1.221",
                        "hypervisorType":"KVM",
                        "state":"Enabled",
                        "status":"Connected",
                        "totalCpuCapacity":240,
                        "availableCpuCapacity":240,
                        "totalMemoryCapacity":540620193792,
                        "availableMemoryCapacity":540620193792,
                        "createDate":"Sep 26, 2016 11:26:02 AM",
                        "lastOpDate":"Sep 27, 2016 11:16:25 PM"
                    }
                ],
            "success":true
            }
        }
        :return:
        '''
        content = {
            "conditions": []
        }

        rsp = self.api_call(self.UUID, "org.zstack.header.host.APIQueryHostMsg", content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)

        print "successfully Query All Host %s" % (rsp)

    def tags_host(self, tags):
        pass

    def logout(self, session_uuid):
        content = {"sessionUuid": session_uuid}
        rsp = self.api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
        self.error_if_fail(rsp)

        print "successfully logout"
        # pass


if __name__ == '__main__':
    new_zs = zstack_host_api()

    # session_uuid = new_zs.login()
    # new_zs.delete_host('96df40c9e1ad4622a5f5504920c628ac')
    new_zs.add_kvm_host('host-yb', 'b0f4a5bc13ca496ca69df5461fe4a442', '10.0.89.18', 'root', 'Skt6edg')
    # new_zs.change_host_state('848520f29011436c8685e520b87dab23', 'enable')
    # new_zs.reconnect_host('848520f29011436c8685e520b87dab23')
    # new_zs.query_all_host()
    # new_zs.query_host_by_ip('10.0.1.221')
    # new_zs.query_host_by_name('host-yb')

    new_zs.logout(new_zs.UUID)