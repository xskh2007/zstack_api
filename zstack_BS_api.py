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

class zstack_backup_storage_api:
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

        rsp, rsp_code = self.api_call(None, "org.zstack.header.identity.APILogInByAccountMsg", content)
        self.error_if_fail(rsp)

        session_uuid = rsp.values()[0]["inventory"]["uuid"]

        print "successfully login, session uuid is: %s" % session_uuid
        return session_uuid

    def add_fusionstor_backupstorage(self, name, url, hostname, username, password):
        pass

    def add_ceph_backupstorage(self, name, url, hostname, username, password):
        pass

    def add_sftp_backupstorage(self, name, url, hostname, username, password):
        '''
        request: {
            "org.zstack.storage.backup.sftp.APIAddSftpBackupStorageMsg": {
                "hostname": "10.0.89.18",
                "username": "root",
                "password": "Skt6edg",
                "type": "SftpBackupStorage",
                "resourceUuid": "8923e38182ca454482d820248ad8a53c",
                "name": "bs-gzp5",
                "description": null,
                "url": "/root",
                "session": {"uuid": "5c54fbf4e8784497a87eab47552a0edc"}
            }
        }
        :param name: 资源名字；
        :param hostname: Sftp服务器的主机名，一般情况需要输入服务器IP；
        :param url: BS存储需要的路径，如“/home”,分区等；
        :param username: Sftp服务器用户名；如“root”
        :param password: Sftp服务器登录密码；
        :return:
        '''
        content = {
            "name": name,
            "url": url,
            "hostname": hostname,
            "username": username,
            "password": password,
            "description": "Add Sftp Backup Storage %s" % name
        }

        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.storage.backup.sftp.APIAddSftpBackupStorageMsg", content)
        if rsp_code == 200:
            # self.error_if_fail(rsp)
            job_uuid = rsp['uuid']
            status = self.query_until_done(job_uuid)
            print "successfully Add Sftp Backup Storage %s, status %s" % (name, status)
        else:
            print "Found Error in API requests.pls check!"

    def delete_backupstorage(self, uuid):
        '''
        request: {
            "org.zstack.header.storage.backup.APIDeleteBackupStorageMsg": {
                "uuid": "8923e38182ca454482d820248ad8a53c",
                "session": {
                  "uuid": "5c54fbf4e8784497a87eab47552a0edc"
                }
            }
        }
        :param uuid: Backup Storage uuid  备份存储的uuid
        :return:
        '''
        content = {
            "uuid": uuid
        }

        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.header.storage.backup.APIDeleteBackupStorageMsg", content)
        if rsp_code == 200:
            # self.error_if_fail(rsp)
            job_uuid = rsp['uuid']
            status = self.query_until_done(job_uuid)
            print "successfully delete Backup Storage %s, status %s" % (uuid, status)
        else:
            print "Found Error in API requests.pls check!"
        # pass

    def change_backupstorage_state(self, uuid, stateEvent):
        '''
        request: {
            "org.zstack.header.storage.backup.APIChangeBackupStorageStateMsg": {
                "session": {"uuid": "f63ca5149b154bc4942c374ca35f1209"},
                "uuid": "82cf947ae8b44c479c5c30d183e7ae39",
                "stateEvent": "disable"
            }
        }
        :param uuid: 备份存储的uuid
        :param stateEvent: enable/disable
        :return:
        '''
        content = {
            "uuid": uuid,
            "stateEvent": stateEvent
        }
        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.header.storage.backup.APIChangeBackupStorageStateMsg", content)
        if rsp_code == 200:
            # self.error_if_fail(rsp)
            job_uuid = rsp['uuid']
            status = self.query_until_done(job_uuid)

            print "successfully Change Backup Storage State %s to %s, status %s" % (uuid, stateEvent, status)
        else:
            print "Found Error in API requests.pls check!"
        # pass

    def reconnect_backupstorage(self, uuid):
        '''
        request: {
            "org.zstack.storage.backup.sftp.APIReconnectSftpBackupStorageMsg": {
                "uuid": "950c512d895d4686aec475555b917ac2",
                "session": {
                  "uuid": "2f918a2b95624f88ae00f524242aeb4a"
                }
            }
        }
        :param uuid: 备份存储的uuid
        :return:
        '''
        content = {
            "uuid": uuid
        }
        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.storage.backup.sftp.APIReconnectSftpBackupStorageMsg", content)
        # self.error_if_fail(rsp)
        job_uuid = rsp['uuid']
        status = self.query_until_done(job_uuid)

        print "successfully Reconnect Primary Storage %s, status %s" % (uuid, status)
        # pass

    def attach_backup_storage_to_zone(self, backupStorageUuid, zoneUuid):
        """
        request:{
            "org.zstack.header.storage.backup.APIAttachBackupStorageToZoneMsg": {
                "zoneUuid": "c9df649b419243b597b1dec99b90833f",
                "backupStorageUuid": "70a82158faf241e98af898a79d906490",
                "session": {
                  "uuid": "2f918a2b95624f88ae00f524242aeb4a"
                }
            }
        }
        :param backupStorageUuid:
        :param zoneUuid:
        :return:
        """
        content = {
            "backupStorageUuid": backupStorageUuid,
            "zoneUuid": zoneUuid
        }

        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.header.storage.backup.APIAttachBackupStorageToZoneMsg", content)
        if rsp_code == 200:
            # self.error_if_fail(rsp)
            job_uuid = rsp['uuid']
            status = self.query_until_done(job_uuid)

            print "successfully Attach Backup Storage To Zone %s to %s, status %s" % (backupStorageUuid, zoneUuid, status)
        else:
            print "Found Error in API requests.pls check!"

    def detach_backup_storage_from_zone(self, backupStorageUuid, zoneUuid):
        """
        request:{
            "org.zstack.header.storage.backup.APIDetachBackupStorageFromZoneMsg": {
                "zoneUuid": "c9df649b419243b597b1dec99b90833f",
                "backupStorageUuid": "70a82158faf241e98af898a79d906490",
                "session": {
                  "uuid": "2f918a2b95624f88ae00f524242aeb4a"
                }
            }
        }
        :param backupStorageUuid:
        :param zoneUuid:
        :return:
        """
        content = {
            "backupStorageUuid": backupStorageUuid,
            "zoneUuid": zoneUuid
        }

        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.header.storage.backup.APIDetachBackupStorageFromZoneMsg",
                                      content)
        if rsp_code == 200:
            # self.error_if_fail(rsp)
            job_uuid = rsp['uuid']
            status = self.query_until_done(job_uuid)

            print "successfully Detach Backup Storage State %s from %s, status %s" % (backupStorageUuid, zoneUuid, status)
        else:
            print "Found Error in API requests.pls check!"

    def query_backupstorage_by_uuid(self, uuid):
        '''
        request: {
            "org.zstack.header.storage.backup.APIQueryBackupStorageMsg": {
                "session": {"uuid": "f63ca5149b154bc4942c374ca35f1209"},
                "conditions": [{"name": "uuid", "value": "70a82158faf241e98af898a79d906490", "op": "="},{"name": "state", "value": "enable", "op": "="}]
            }
        }
        :param name: Backup Storage 名称
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
        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.header.storage.backup.APIQueryBackupStorageMsg", content)
        if rsp_code == 200:
            self.error_if_fail(rsp)
            # job_uuid = rsp['uuid']
            # status = self.query_until_done(job_uuid)

            print "successfully query Backup Storage by uuid %s, result: %s" % (uuid, rsp)
            return rsp
        else:
            print "Found Error in API requests. Pls check!"

    def query_backupstorage_by_name(self, name):
        '''
        request: {
            "org.zstack.header.storage.backup.APIQueryBackupStorageMsg": {
                "session": {"uuid": "f63ca5149b154bc4942c374ca35f1209"},
                "conditions": [{"name": "name", "value": "zone-yu", "op": "="},{"name": "state", "value": "enable", "op": "="}]
            }
        }
        :param name: Backup Storage 名称
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
        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.header.storage.backup.APIQueryBackupStorageMsg", content)
        if rsp_code == 200:
            self.error_if_fail(rsp)
            # job_uuid = rsp['uuid']
            # status = self.query_until_done(job_uuid)

            print "successfully query Backup Storage by name %s, result: %s" % (name, rsp)
            return rsp
        else:
            print "Found Error in API requests. Pls check!"

    # Query Backup Storage
    def query_all_backupstorage(self):
        '''
        request: {
            "org.zstack.header.storage.backup.APIQueryBackupStorageMsg": {
                "session": {"uuid": "f63ca5149b154bc4942c374ca35f1209"},
                "conditions": []
            }
        }
        :return:
        '''
        content = {
            "conditions": []
        }

        rsp, rsp_code = self.api_call(self.UUID, "org.zstack.header.storage.backup.APIQueryBackupStorageMsg", content)
        if rsp_code == 200:
            self.error_if_fail(rsp)
            # job_uuid = rsp['uuid']
            # status = self.query_until_done(job_uuid)
            print "successfully Query All Backup Storage %s" % (rsp)
            return rsp
        else:
            print "Found Error in API requests. Pls check!"

    def tags_host(self, tags):
        pass

    def logout(self, session_uuid):
        content = {"sessionUuid": session_uuid}
        rsp, rsp_code = self.api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
        if rsp_code == 200:
            self.error_if_fail(rsp)
            print "successfully logout"
        else:
            print "Found Error in API requests. Pls check"


if __name__ == '__main__':
    new_zs = zstack_backup_storage_api()

    # session_uuid = new_zs.login()
    # new_zs.add_sftp_backupstorage('bs_yuan', '/root', '10.0.89.18', 'root', 'Skt6edg')
    # new_zs.delete_backupstorage('0e3292931b88447cb991483890df404c')
    # new_zs.change_backupstorage_state('70a82158faf241e98af898a79d906490', 'enable')
    # new_zs.reconnect_backupstorage('70a82158faf241e98af898a79d906490')
    # new_zs.detach_backup_storage_from_zone('70a82158faf241e98af898a79d906490', 'c9df649b419243b597b1dec99b90833f')
    # new_zs.attach_backup_storage_to_zone('70a82158faf241e98af898a79d906490', 'c9df649b419243b597b1dec99b90833f')
    # new_zs.query_all_backupstorage()
    new_zs.query_backupstorage_by_uuid(uuid='70a82158faf241e98af898a79d906490')
    # new_zs.query_backupstorage_by_name('Backup_Storage-1')

    new_zs.logout(new_zs.UUID)
