from flask import Flask, request, jsonify
from wxcloudrun import app
import requests
# 创建应用实例
import sys


app = Flask(__name__)

# 这里的 'YOUR_TOKEN' 需要替换为您的 ChatGPT API token
CHATGPT_API_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJjaHc5NjEyNkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJwb2lkIjoib3JnLVJOQ09DcW8xTlBXZlc0V2hNSUdKYkFaQyIsInVzZXJfaWQiOiJ1c2VyLVFJNllCTlJpbEc0RUpzdWV0NHRGUGRiQyJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI0OTc4NDQwMDgwNTUwNzkxOTMiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzA5NjkxMTEyLCJleHAiOjE3MTA1NTUxMTIsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.HETYGljFEsGurGdqKwWNLxxVkTSfO30tHw0Ub5fjkGMSxaJtaw7WExc7uV36e7KA8oys_H3DftTBHhVxcWWM6iRDV3FzUg2Qr9EMWS5uGTPOVfNGueHQ5DUXyIzCEgHVhvef8kvvuW0F_LpWx_ip8dCLvVh-YtYSsgsEEavjgfc-yiOlNuJhqPSCwlYWF3S0omW6D5gzzBM5LugUepWXorHBCdG59gIt__NnM1GfnU9vhT70m07kJT8ap2J7AoRZB4xOifZMVe_LNfUA2U-iQVzDOZUE42JMsiXHcHVbbSMt6WKvRmMO9EgKh9pbT7H7s6k6qpACWTkiF2fbVerH7A'
CHATGPT_API_URL = 'https://api.openai.com/v1/engines/davinci-codex/completions'


# 发送消息
@app.route('/wechatGpt', methods=['POST'])
def wechat():
    data = request.json
    wechat_message = data.get('message', '')

    # 这里可以打印日志
    print(request)
    print(wechat_message)

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

    gpt_text = chatgpt_response.get('choices', [{}])[0].get('text', '')

    # 这里应该编写正确对接微信API的代码，以下为示例，假定有一个函数 send_wechat_response 来发送回复
    wechat_api_response = send_wechat_response(wechat_message, gpt_text)

    return jsonify(wechat_api_response)


def send_wechat_response(user_message, gpt_response):
    # 这里应当使用微信公众号的 API 来发送回复
    url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send'

    # 构造回复用户的消息数据格式，以下仅为示例
    wechat_response_data = {
        'touser': user_message['FromUserName'],  # 你需要从用户发送的消息中获取 FromUserName
        'msgtype': 'text',
        'text': {
            'content': gpt_response
        }
    }

    # 发送 POST 请求到微信API
    response = requests.post(url, json=wechat_response_data)
    return response.json()


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2], debug=True)