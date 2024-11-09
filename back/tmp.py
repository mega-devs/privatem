import requests
import mailer
from flask_socketio import SocketIO, send
from flask import Flask, request

# res = requests.post('http://127.0.0.1:5000/api/login', json={'name': 'root', 'password': 'root'})
# print(res.text)

# res = requests.post('http://127.0.0.1:5000/api/session/add', json={'name': 'test', 'token': 'rzyxrgbshrvsufzs'})
# print(res.text)

# res = requests.get('http://127.0.0.1:5000/api/session/list')
# print(res.text)

# rzyxrgbshrvsufzs

res = requests.post('http://185.196.11.95:5001/api/input/material'
                    , json={'token': 'epqptvgwaimixqzm', 'session': 'test',
                    'type': 'domains',
                    'file': 'https://t1p-cc.aws.seis.co.ke/reviewed,3439\nhttps://shiro.huntifyllc.com/cons_rings_requiring_4711_childhood_tabs_fetish_revenues.asp\nhttps://www.youtube.com'})
print(res.text)

# res = requests.post('http://127.0.0.1:5000/api/reset/del', json={'token': 'rzyxrgbshrvsufzs',
#                     'type': 'all', 'session': 'test'})
# print(res.text)

# app = Flask(__name__)
# socket = SocketIO(app, cors_allowed_origins='*')
# mailer.check_domain(socket, 'test', 'all')

