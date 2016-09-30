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

class zstack_zone_api:
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

    def create_zone(self, name='zone-default'):
        content = {"name": name}

        rsp = self.api_call(self.UUID, "org.zstack.header.zone.APICreateZoneMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully created %s, status %s" % (name, status)
        # pass

    def delete_zone(self, uuid):
        content = {"uuid": uuid}

        rsp = self.api_call(self.UUID, "org.zstack.header.zone.APIDeleteZoneMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)
        print "successfully delete %s, status %s" % (uuid, status)

        # return self.UUID
        # pass

    def logout(self, session_uuid):
        content = {"sessionUuid": session_uuid}
        rsp = self.api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
        self.error_if_fail(rsp)

        print "successfully logout"
        # pass

    def query_zone_by_uuid(self, uuid):
        content = {"conditions": [{"name": "uuid", "value": uuid,"op": "="}]}

        # {"org.zstack.header.zone.APIQueryZoneMsg": {
        #     "session":{"uuid": "a8b1af68e3f047db9e0f8d3ee5287b82"},
        #     "conditions": [{"name": "uuid", "value": "cb456242d027469d9837889a7cea7930","op": "="}]
        #     }
        # }

        rsp = self.api_call(self.UUID, "org.zstack.header.zone.APIQueryZoneMsg", content)
        # self.error_if_fail(rsp)


        print "successfully query zone"
        try:
            result = rsp['org.zstack.header.zone.APIQueryZoneReply']['inventories']
            print "zone total: ", len(result)
        except:
            print "The zone uuid is not esxits!"
        print result

        return result

    def query_zone_by_name(self, name):
        result = {}
        # {"org.zstack.header.zone.APIQueryZoneMsg": {
        #     "session":{"uuid": "a8b1af68e3f047db9e0f8d3ee5287b82"},
        #     "conditions": [{"name": "name", "value": "zone-zb","op": "="}]
        #     }
        # }
        content = {"conditions": [{"name": "name", "value": name, "op": "="}]}
        rsp = self.api_call(self.UUID, "org.zstack.header.zone.APIQueryZoneMsg", content)
        print "successfully query zone"
        try:
            result = rsp['org.zstack.header.zone.APIQueryZoneReply']['inventories']
            print "zone total: ", len(result)
        except:
            print "The zone is not esxits."
        print result

        return result
        # pass

    def query_all_zone(self):
        result = {}
        content = {"conditions": []}
        rsp = self.api_call(self.UUID, "org.zstack.header.zone.APIQueryZoneMsg", content)
        print "successfully query zone"
        try:
            result = rsp['org.zstack.header.zone.APIQueryZoneReply']['inventories']
            print "zone total: ", len(result)
        except:
            print "The zone is not esxits."
        print result

        return result
        # pass


if __name__ == '__main__':
    new_zs = zstack_api()
    # session_uuid = new_zs.login()
    # new_zs.delete_zone("2019f967c0f3418da86b9aca6c88f30c")
    new_zs.create_zone('zone_alone')
    # new_zs.query_zone_by_uuid('5c844020236d45cc8d5a47d6102cd756')
    # zone_list = new_zs.query_zone_by_name('zone_alone')
    # for zone in zone_list:
    #     new_zs.delete_zone(zone['uuid'])
    # new_zs.query_all_zone()
    new_zs.logout(new_zs.UUID)