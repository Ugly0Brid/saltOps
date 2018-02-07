import urllib, yaml, json
import requests

requests.packages.urllib3.disable_warnings()


class salt_api_token(object):
    """
    list_all = salt_api_token({'fun': 'cmd.run', 'tgt': node_list,
                                       'arg': cmd    },
                                      salt_api_url, {'X-Auth-Token' : token_api_id})
    """

    def __init__(self, data, url, token=None):
        self.data = data
        self.url = url
        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            "Accept": "application/x-yaml",
        }
        s = {"client": "local_async"}
        self.headers.update(token)
        self.data.update(s)

    def loadJob(self, jid):
        """
        加载作业信息
        :param jid:
        :return:
        """
        req = requests.get(self.url + '/jobs/' + jid, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)

    def run(self):
        """
        异步执行任务
        :return:
        """
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)

    def CmdRun(self, client='local'):
        """
        同步执行任务
        :return:
        """
        self.data["client"] = client
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)

    def wheelRun(self):
        self.data["client"] = "wheel"
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)

    def sshRun(self):
        """
        SSH模式执行任务
        :return:
        """
        self.data["client"] = "ssh"
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)

    def runnerRun(self):
        """
        使用Runner客户端执行
        :return:
        """
        self.data["client"] = "runner"
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)
