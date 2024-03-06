from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 这里的 'YOUR_TOKEN' 需要替换为您的 ChatGPT API token
CHATGPT_API_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJjaHc5NjEyNkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJwb2lkIjoib3JnLVJOQ09DcW8xTlBXZlc0V2hNSUdKYkFaQyIsInVzZXJfaWQiOiJ1c2VyLVFJNllCTlJpbEc0RUpzdWV0NHRGUGRiQyJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI0OTc4NDQwMDgwNTUwNzkxOTMiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzA5NjkxMTEyLCJleHAiOjE3MTA1NTUxMTIsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.HETYGljFEsGurGdqKwWNLxxVkTSfO30tHw0Ub5fjkGMSxaJtaw7WExc7uV36e7KA8oys_H3DftTBHhVxcWWM6iRDV3FzUg2Qr9EMWS5uGTPOVfNGueHQ5DUXyIzCEgHVhvef8kvvuW0F_LpWx_ip8dCLvVh-YtYSsgsEEavjgfc-yiOlNuJhqPSCwlYWF3S0omW6D5gzzBM5LugUepWXorHBCdG59gIt__NnM1GfnU9vhT70m07kJT8ap2J7AoRZB4xOifZMVe_LNfUA2U-iQVzDOZUE42JMsiXHcHVbbSMt6WKvRmMO9EgKh9pbT7H7s6k6qpACWTkiF2fbVerH7A'
CHATGPT_API_URL = 'https://api.openai.com/v1/engines/davinci-codex/completions'


# 发送消息
def send_wechat_message(openid, access_token, message):
    url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}'
    headers = {'Content-Type': 'application/json'}

    data = {
        'touser': openid,  # 用户的 OpenID
        'msgtype': 'text',  # 消息类型
        'text': {
            'content': message  # 要发送的消息内容
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


# 微信订阅号的消息接口
@app.route('/wechatGpt', methods=['POST'])
def wechat():
    data = request.json
    # 这里应该提取微信发来的消息并进行处理，以下仅为示例
    wechat_message = data.get('message', '')

    # ChatGPT API 请求的头部信息
    headers = {
        'Authorization': f'Bearer {CHATGPT_API_TOKEN}',
        'Content-Type': 'application/json'
    }

    # 获取 ChatGPT 的回复
    chatgpt_response = requests.post(
        CHATGPT_API_URL,
        headers=headers,
        json={'prompt': wechat_message, 'max_tokens': 1500}
    ).json()

    # 从 ChatGPT 的回复中提取文本部分
    gpt_text = chatgpt_response.get('choices', [{}])[0].get('text', '')

    # 将 ChatGPT 的回复发送回微信订阅号，这里需要对接您的微信API
    # 并确保按照微信API所需的格式发送消息，以下仅为示例，'YOUR_WECHAT_API'需替换为实际API
    wechat_api_response = requests.post('YOUR_WECHAT_API', json={'reply': gpt_text}).json()

    return jsonify(wechat_api_response)


app = Flask(__name__)


@app.route('/wechat_msg_check', methods=['POST'])
def wechat_msg_check():
    openid = request.headers.get('x-wx-openid')
    content = request.json.get('content')

    url = 'http://api.weixin.qq.com/wxa/msg_sec_check'  # 由于是云调用，不需要 access_token
    data = {
        'openid': openid,
        'version': 2,
        'scene': 2,
        'content': content
    }

    response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        # 打印接口返回内容，便于调试
        print('接口返回内容', response.json())
        return jsonify(response.json()), 200
    else:
        return 'Error', response.status_code


if __name__ == '__main__':
    app.run()