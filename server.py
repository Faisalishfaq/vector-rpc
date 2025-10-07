# server.py
import time
from flask import Flask, request, jsonify
from vector_clock import VectorClock
import os

app = Flask(__name__)

SERVER_ID = os.environ.get('SERVER_ID', 'server')
server_vc = VectorClock(pid=SERVER_ID)

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{ts}] {msg}", flush=True)
    
#  new route add 
@app.route('/')
def home():
    return " Vector Clock RPC Server is running successfully!"


@app.route('/rpc', methods=['POST'])
def rpc():
    data = request.get_json() or {}
    sender = data.get('sender_id', 'unknown')
    client_vc = data.get('vector_clock', {})

    log(f"Received RPC from {sender} with VC={client_vc}")

    # merge then increment (receive rule)
    server_vc.merge(client_vc)
    server_vc.increment(SERVER_ID)
    log(f"Server VC after merge+increment: {server_vc.to_dict()}")
    payload = data.get('payload', {})
    result = {'echo': payload, 'server_time': time.time()}

    return jsonify({
        'vector_clock': server_vc.to_dict(),
        'result': result
    })

@app.route('/vc', methods=['GET'])
def get_vc():
    return jsonify({'vector_clock': server_vc.to_dict()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    log(f"Starting server on 0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
