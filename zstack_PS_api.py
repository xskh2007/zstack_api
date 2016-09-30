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

class zstack_primarystorage_api:
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

    def add_nfs_primarystorage(self, name, zoneUuid, url):

        content = {
            "name": name,
            "url": url,
            "zoneUuid": zoneUuid,
            "description": "Add NFS Primary Storage %s" % name
        }

        rsp = self.api_call(self.UUID, "org.zstack.storage.primary.local.APIAddNfsPrimaryStorageMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully Add NFS Primary Storage %s, status %s" % (name, status)
        # pass

    def add_local_primarystorage(self, name, zoneUuid, url):
        '''
        request: {
            "org.zstack.storage.primary.local.APIAddLocalPrimaryStorageMsg": {
                "url": "/home",
                "zoneUuid": "4cc9847534384039b323e8d2fff4b606",
                "name": "localPrimarySotrage01",
                "session": {"uuid": "f63ca5149b154bc4942c374ca35f1209"}
            }
        }
        :param name: 资源名字；
        :param zoneUuid: 父区域的uuid；
        :param url: 本地存储需要的路径，如“/home”,分区等；
        :return:
        '''
        content = {
            "name": name,
            "url": url,
            "zoneUuid": zoneUuid,
            "description": "Add local Primary Storage %s" % name
        }

        rsp = self.api_call(self.UUID, "org.zstack.storage.primary.local.APIAddLocalPrimaryStorageMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully Add local Primary Storage %s, status %s" % (name, status)

    def delete_primarystorage(self, uuid):
        '''
        request: {
            "org.zstack.header.storage.primary.APIDeletePrimaryStorageMsg": {
                "uuid": "77b820cf4bc247048c4495207be5a34e",
                "session": {"uuid": "460369df1444440c8fe8560af425bd81"}
            }
        }
        :param uuid: Primary Storage uuid
        :return:
        '''
        content = {
            "uuid": uuid
        }

        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIDeletePrimaryStorageMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully delete Primary Storage %s, status %s" % (uuid, status)

        # return self.UUID
        # pass

    def change_primarystorage_state(self, uuid, stateEvent):
        '''
        request: {
            "org.zstack.header.storage.primary.APIChangePrimaryStorageStateMsg": {
                "session": {"uuid": "f63ca5149b154bc4942c374ca35f1209"},
                "uuid": "82cf947ae8b44c479c5c30d183e7ae39",
                "stateEvent": "disable"
            }
        }
        :param uuid: 主机的uuid
        :param stateEvent: enable/disable
        :return:
        '''
        content = {
            "uuid": uuid,
            "stateEvent": stateEvent
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIChangePrimaryStorageStateMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully Change Primary Storage State %s to %s, status %s" % (uuid, stateEvent, status)
        # pass

    def reconnect_primarystorage(self, uuid):
        '''
        request: {
            "org.zstack.header.storage.primary.APIReconnectPrimaryStorageMsg": {
                "uuid": "82cf947ae8b44c479c5c30d183e7ae39",
                "session": {"uuid": "460369df1444440c8fe8560af425bd81"}
            }
        }
        :param uuid: 主存储的uuid
        :return:
        '''
        content = {
            "uuid": uuid
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIReconnectPrimaryStorageMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully Reconnect Primary Storage %s, status %s" % (uuid, status)
        # pass

    def query_primarystorage_by_uuid(self, uuid):
        '''
        request: {
            "org.zstack.header.storage.primary.APIQueryPrimaryStorageMsg": {
                "session": {"uuid": "f925c7ebb98245ac9a78d0e7a37cb890"},
                "conditions": [{"name": "uuid", "value": "82cf947ae8b44c479c5c30d183e7ae39", "op": "="}]
            }
        }
        :param managementIP:
        :return:
        '''
        content = {
            "conditions": [
                {
                    "name": "uuid",
                    "value": uuid,
                    "op": "="
                }
            ]
        }
        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIQueryPrimaryStorageMsg", content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)

        print "successfully query Primary Storage by uuid %s, result: %s" % (uuid, rsp)
        return rsp
        # pass

    def query_primarystorage_by_name(self, name):
        '''
            request: {
                "org.zstack.header.storage.primary.APIQueryPrimaryStorageMsg": {
                    "session": {"uuid": "f925c7ebb98245ac9a78d0e7a37cb890"},
                    "conditions": [{"name": "name", "value": "ps-yuan", "op": "="}]
                }
            }
            :param name: Primary Storage 名称
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
        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIQueryPrimaryStorageMsg", content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)

        print "successfully query Primary Storage by name %s, result: %s" % (name, rsp)
        return rsp

    def query_all_primarystorage(self):
        '''
        request: {
            "org.zstack.header.storage.primary.APIQueryPrimaryStorageMsg": {
                "session": {"uuid": "f63ca5149b154bc4942c374ca35f1209"},
                "conditions": []
            }
        }
        :return:
        '''
        content = {
            "conditions": []
        }

        rsp = self.api_call(self.UUID, "org.zstack.header.storage.primary.APIQueryPrimaryStorageMsg", content)
        self.error_if_fail(rsp)
        # job_uuid = rsp['uuid']
        # status = self.query_until_done(job_uuid)

        print "successfully Query All Primary Storage %s" % (rsp)
        return rsp

    def tags_host(self, tags):
        pass

    def logout(self, session_uuid):
        content = {"sessionUuid": session_uuid}
        rsp = self.api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
        self.error_if_fail(rsp)

        print "successfully logout"
        # pass


if __name__ == '__main__':
    new_zs = zstack_primarystorage_api()

    # session_uuid = new_zs.login()
    # new_zs.add_local_primarystorage('ps-yuan', 'c9df649b419243b597b1dec99b90833f', url='/home')
    # new_zs.delete_primarystorage('8352683f89fa46ad843986d54d2bbc31')
    # new_zs.change_primarystorage_state('82cf947ae8b44c479c5c30d183e7ae39', 'enable')
    # new_zs.reconnect_primarystorage('82cf947ae8b44c479c5c30d183e7ae39')
    # new_zs.query_all_primarystorage()
    new_zs.query_primarystorage_by_name('ps-yuan')
    new_zs.query_primarystorage_by_uuid('82cf947ae8b44c479c5c30d183e7ae39')

    new_zs.logout(new_zs.UUID)