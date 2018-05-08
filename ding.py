# coding:utf-8
import json
import requests
"""
创建回话，加入管理员，有了会话id，才能发送
ref: https://github.com/bluetom520/dingding/blob/master/dingding.py
"""


class Ding(object):

    def __init__(self, corp_id, corp_secret, agent_id):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.agent_id = agent_id
        self.token_url = 'https://oapi.dingtalk.com/gettoken'
        self.get_dept_list_url = 'https://oapi.dingtalk.com/department/list'
        self.url_send = 'https://oapi.dingtalk.com/message/send'
        self.__params = {
            "corpid": self.corp_id,
            "corpsecret": self.corp_secret
        }

        self.access_token = self.get_access_token()
        self.token_params = {
            'access_token': self.access_token
        }

    def get_access_token(self):
        headers = {'content-type': 'application/json'}
        res = requests.get(self.token_url, headers=headers, params=self.__params)
        return res.json()['access_token']

    def get_dept_list(self):
        res = requests.get(self.get_dept_list_url, params=self.token_params)
        return res.json()['department']

    def send_text_message(self, content, userid='', toparty=''):
        payload = {
            'touser': userid,
            'toparty': toparty,
            'agentid': self.agent_id,

            "msgtype": "text",
            "text": {
                'content': content
            }
        }
        headers = {'content-type': 'application/json'}
        params = self.token_params
        res = requests.post(self.url_send, headers=headers, params=params, data=json.dumps(payload))
        return res.json()


class DingHK(object):
    """webbook 调用发送到群组"""

    def __init__(self, access_token):
        self.send_url = "https://oapi.dingtalk.com/robot/send"
        self.access_token = access_token
        self.__params = {
            'access_token': access_token
        }

    def send_text(self, content):
        headers = {'content-type': 'application/json'}
        payload = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        res = requests.post(self.send_url, headers=headers,
                            params=self.__params,
                            data=json.dumps(payload))
        return res.json()
