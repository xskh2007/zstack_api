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

class zstack_base_api:
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

    def query_until_done_other(self, job_uuid):
        # conn.request("GET", "/zstack/api/result/%s" % job_uuid)
        request = requests.get(self.url_result + str(job_uuid))

        response = json.loads(request.content)
        # rsp = json.loads(rsp_body)
        if response["state"] == "Done":
            return response

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

    def api_call_other(self, session_uuid, api_id, api_content):
        if session_uuid:
            api_content["session"] = {"uuid": session_uuid}
        api_body = {api_id: api_content}

        request = requests.post(self.url, data=json.dumps(api_body), headers=self.header)
        response = json.loads(request.content)
        response_code = request.status_code
        if "result" in response.keys():
            result = json.loads(response['result'])
        else:
            result = response
        return result, response_code

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

    def logout(self, session_uuid):
        content = {"sessionUuid": session_uuid}
        rsp = self.api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
        self.error_if_fail(rsp)

        print "successfully logout"
        # pass


if __name__ == '__main__':
    new_zs = zstack_base_api()

    session_uuid = new_zs.login()
    # new_zs.create_vminstance(name='vm-api',
    #                          instanceOfferingUuid='545a4cc398064c469ed498f5bd392c95',
    #                          l3NetworkUuids='235ee7cfc64e4fd1a2aa1ad8f55cba03',
    #                          imageUuid='ac57e254210e479b9050dc6c1cc10e8d',
    #                          hostUuid='f3e90e2620f840618a8941b6688101b9',
    #                          clusterUuid='f6cf5efe72924ccf90b771d32f610f19',
    #                          zoneUuid='	4cc9847534384039b323e8d2fff4b606')
    # new_zs.delete_primarystorage('8352683f89fa46ad843986d54d2bbc31')
    # new_zs.change_primarystorage_state('82cf947ae8b44c479c5c30d183e7ae39', 'enable')
    # new_zs.reconnect_primarystorage('82cf947ae8b44c479c5c30d183e7ae39')
    # new_zs.query_all_primarystorage()

    new_zs.logout(new_zs.UUID)