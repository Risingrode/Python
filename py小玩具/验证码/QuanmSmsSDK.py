# -*- coding: utf-8 -*-
# author:Tiper(邱鹏)
# 文件所属项目:QDC SMS SDK
# 文件描述:QuanmSMS SDK (泉鸣开放平台sms接口SDK)，包含执行短信业务所需的方法
# Python版本要求：Python3及以上（可自行修改兼容Python2）
# 官网：dev.quanmwl.com
# 发布日期:2022-7-31

import random
import hashlib
import requests

hl = hashlib.md5()


class SDK:
    def __init__(self):
        # 请开发者修改下列三行配置信息
        self.open_id = '87'   # 开发者ID
        self.api_key = '5a39ddbb341111ed86b4ad248584d5b4'   # 能力列表的apiKey
        self.def_model_id = 0    # 默认情况下使用的模板ID
        self.api_host = 'http://dev.quanmwl.com'  # Api Host【默认，api支持https，如有需要请修改】

        self.state_code = {
            '200': '短信发送成功',
            '201': '表单信息或接口信息有误',
            '202': '信息重复',
            '203': '服务器异常，请稍后重试',
            '204': '找不到数据',
            '205': '本次请求不安全',
            '206': '接口版本过低',
            '207': '余额不足',
            '208': '验签失败',
            '209': '功能被禁用',
            '210': '账户被禁用',
            '211': '参数过长',
            '212': '权限不足',
            '213': '参数调用状态异常',
            '214': '版本过高',
            '215': '内容受限',
            '216': '内容违规',
            '???': '严重未知错误，请联系服务提供商'
        }
        # 更多状态：https://quanmwl.yuque.com/docs/share/9fbd5429-6575-403d-8a3d-7081b2977eda?#8sz4 《平台状态码处理指引》

    def sign(self, _tel, model_id, model_args):
        # type:(str, str, str) -> str
        """
        签名方法
        :param _tel: 接收者手机号
        :param model_id: 短信模板ID
        :param model_args: 短信模板变量参数字典
        :return:
        """
        server_sign_data = f"{self.open_id}{self.api_key}{_tel}{model_id}{model_args}"
        hl.update(server_sign_data.encode("utf-8"))
        return hl.hexdigest()

    def send(self, tel, model_id, model_args):
        # type:(str, int, dict) -> tuple[bool, str]
        """
        发送短信
        :param tel: 接收者手机号
        :param model_id: 短信模板ID
        :param model_args: 短信模板变量参数字典
        :return:
        """
        headers = {
            'User-Agent': 'QuanmOpenApi Python SDK',  # 非必要
        }

        data = {
            'openID': self.open_id,
            'tel': tel,
            'sign': self.sign(tel, str(model_id), str(model_args).replace(' ', '')),
            'model_id': model_id,
            'model_args': f'{model_args}'
        }
        try:
            response = requests.post(f'{self.api_host}/v1/sms', headers=headers, data=data)
            # http_status = response.status_code  几乎可以不依赖http状态码，如有需要请自行修改
        except:
            return False, 'Server Error'
        _mess = 'Not Find'
        if response is None or 'HTML>' in response.text:
            print("Requests Fail")
            return False, _mess
        else:
            redata = eval(response.text)

            http_state = response.status_code
            if http_state != 200 and 'state' not in redata:
                return False, _mess

            api_state = redata['state']
            if api_state in self.state_code:
                _mess = self.state_code[api_state]
            if api_state == '200':
                return True, _mess
            else:
                return True, _mess


if __name__ == '__main__':
    sms = SDK()  # 实例化SDK
    # 这里演示了一个简单的验证码功能
    check_code = random.randint(100000, 999999)  # 生成验证码
    results, info = sms.send('17526672912', sms.def_model_id, {'code': check_code})  # 发送
    print(info)
