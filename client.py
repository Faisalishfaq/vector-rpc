# client.py
import argparse, json, os, requests, time
from vector_clock import VectorClock

STATE_DIR = ".client_state"

def state_file(client_id):
    os.makedirs(STATE_DIR, exist_ok=True)
    return os.path.join(STATE_DIR, f"{client_id}.json")

def load_vc(client_id):
    f = state_file(client_id)
    if os.path.exists(f):
        return json.load(open(f))
    else:
        return {}

def save_vc(client_id, vc):
    json.dump(vc, open(state_file(client_id), "w"), indent=2)

def send(server_url, client_id, payload):
    vc_dict = load_vc(client_id)
    vc = VectorClock(pid=client_id, clock=vc_dict)
    vc.increment(client_id)  # increment before send
    save_vc(client_id, vc.to_dict())
    print(f"[{client_id}] Sending with VC={vc.to_dict()} payload={payload}")

    r = requests.post(server_url.rstrip('/') + '/rpc', json={
        'sender_id': client_id,
        'vector_clock': vc.to_dict(),
        'payload': payload
    }, timeout=10)
    data = r.json()
    print(f"[{client_id}] Received server VC={data.get('vector_clock')}")
    vc.merge(data.get('vector_clock', {}))
    save_vc(client_id, vc.to_dict())
    print(f"[{client_id}] After merge, VC={vc.to_dict()}")
    return data

def fetch_server_vc(server_url):
    r = requests.get(server_url.rstrip('/') + '/vc', timeout=10)
    return r.json().get('vector_clock', {})

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--id', required=True, help='client id (A/B/...)')
    p.add_argument('--server', default='http://localhost:5000', help='server URL')
    p.add_argument('action', choices=['send', 'get-vc', 'fetch-and-merge'], help='action')
    p.add_argument('--msg', default='hello', help='payload message')
    args = p.parse_args()

    if args.action == 'send':
        send(args.server, args.id, {'msg': args.msg})
    elif args.action == 'get-vc':
        print(fetch_server_vc(args.server))
    elif args.action == 'fetch-and-merge':
        sv = fetch_server_vc(args.server)
        vc = VectorClock(pid=args.id, clock=load_vc(args.id))
        print(f"[{args.id}] before merge {vc.to_dict()}")
        vc.merge(sv)
        save_vc(args.id, vc.to_dict())
        print(f"[{args.id}] after merge {vc.to_dict()}")

if __name__ == '__main__':
    main()
