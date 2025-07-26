from flask import Flask, render_template,request,send_file
from flask_socketio import SocketIO, emit
import uuid
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 存储客户端会话
clients = {}

@app.route('/')
def index():
    return send_file('index.html')

@socketio.on('connect')
def handle_connect():
    while True:
        client_id = str(random.randint(100, 9999))
        if client_id not in clients:
            break
    clients[client_id] = {'sid': request.sid}
    emit('client_id', {'id': client_id})

@socketio.on('disconnect')
def handle_disconnect():
    for client_id, client in clients.items():
        if client['sid'] == request.sid:
            del clients[client_id]
            break

# 封装查找目标id的逻辑
def find_client_sid(target_id):
    return clients.get(target_id, {}).get('sid')

@socketio.on('offer')
def handle_offer(data):
    target_id = data['target_id']
    offer = data['offer']
    target_sid = find_client_sid(target_id)
    if target_sid:
        socketio.emit('offer', {'sender_id': data['sender_id'], 'offer': offer}, to=target_sid)

@socketio.on('answer')
def handle_answer(data):
    target_id = data['target_id']
    answer = data['answer']
    target_sid = find_client_sid(target_id)
    if target_sid:
        socketio.emit('answer', {'sender_id': data['sender_id'], 'answer': answer}, to=target_sid)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    target_id = data['target_id']
    candidate = data['candidate']
    target_sid = find_client_sid(target_id)
    if target_sid:
        socketio.emit('ice_candidate', {'sender_id': data['sender_id'], 'candidate': candidate}, to=target_sid)

if __name__ == '__main__':
    socketio.run(app, debug=True,host='0.0.0.0',port=5000)
#http://192.168.0.100:5000