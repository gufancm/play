
# 宝龙悠悠

# 宝龙悠悠仅支持py环境
# 完成自动签到

# 自行捉包
# https://proservice.powerlong.com/member/refresh/token里面uid，token，openid填到变量 BlyyUsers 中, 多账号用回车分隔或逗号分隔
# export BlyyUsers="uid#token#openid"

# cron: 0 0 8 * * ?  每天上午八点执行一次即可



import os
import requests

# 获取环境变量中的用户列表
users = os.environ.get('BlyyUsers').split('\n')

# 构造PushPlus的请求参数
pushplus_token = os.environ.get('PUSH_PLUS_TOKEN')
data = {
    "token": pushplus_token,
    "title": "宝龙签到",
    "content": ""
}

# 刷新 token
def refresh_token(uid, token, openid):
    url = 'https://proservice.powerlong.com/member/refresh/token'
    headers = {
        'Host': 'proservice.powerlong.com',
        'Connection': 'keep-alive',
        'Content-Length': '468',
        'platformType': '1',
        'content-type': 'application/json',
        'uid': uid,
        'token': token,
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d38) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxefc15bc9d0cb36b1/217/page-frame.html'
    }
    data = {
        "miniAppKey": "MAIN_MINIAPP",
        "projectId": "402834702ec49066012ed7a1aac1225e",
        "uid": uid,
        "openId": openid,
        "sign": "0990a1ea5e7aca718b872b3ee83c553142753313",
        "encryptedData": "TWY/+Y2hgY5jcvMLAjEk5wQRSA24Isw0p7KX+LzL5tdrGXXyKrunUSDPq7NGxjUAQ07I0GcnI5U6x8hSWt8ggiuCJE4Ko0EhlVqJhWtp2nl2KpO47qp6U1ySNd5a9tiUhN2hoDGw2ew6P0sj0vANd3qLJIF3B/bDcljOukeiv2F3kPzn66uKBdIr17K4wcYgQaXbFcaf304XOev0XHWw5g==",
        "timestamp": 1687746635295
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result['code'] == 200:
            new_token = result['data']['token']
            return new_token
        else:
            print('刷新 token 失败！')
    else:
        print('请求失败！')
    return None

# 进行签到
def signin(uid, token, openid, index):
    url = f'https://proservice.powerlong.com/signinApply/doWiexinSignin?miniAppKey=MAIN_MINIAPP&projectId=402834702ec49066012ed7a1aac1225e&uid={uid}'
    headers = {
        'Host': 'proservice.powerlong.com',
        'Connection': 'keep-alive',
        'platformType': '1',
        'content-type': 'application/json',
        'uid': uid,
        'token': token,
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d38) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxefc15bc9d0cb36b1/217/page-frame.html'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if result['code'] == 200:
            integral = result['data']['integral']
            extraintegral = result['data']['extraintegral']
            extraperiod = result['data']['extraperiod']
            print(f'账号{index + 1} 签到成功！')
            print('积分:', integral)
            print('额外积分:', extraintegral)
            print('额外积分有效期:', extraperiod)
            return True
        else:
            if result['code'] == -2:
                print(f'账号{index + 1} 失效，请重新抓包')
            else:
                print(f'账号{index + 1} 签到失败！')
                print('错误消息:', result['messageToUser'])
    else:
        print('请求失败！')
    return False

# 遍历用户列表，对每个用户进行签到
for index, user in enumerate(users):
    # 解析用户信息
    uid, token, openid = user.split('#')

    # 刷新 token
    new_token = refresh_token(uid, token, openid)
    if new_token:
        # 更新 token 后进行签到
        success = signin(uid, new_token, openid, index)

        # 拼接推送内容
        status = "签到成功！" if success else "签到失败！"
        content = f"账号{index + 1}，签到状态: {status}\n"
        data['content'] += content

# 发送推送请求
url = 'http://www.pushplus.plus/send'
response = requests.post(url, data=data)

# 输出推送响应结果
print(f'推送响应：{response.text}')
