# VectorClock RPC Project (Full Docker Version)

## Project structure
```
vectorclock-rpc/
  ├─ server.py
  ├─ client.py
  ├─ vector_clock.py
  ├─ requirements.txt
  ├─ Dockerfile
  ├─ .gitignore
  ├─ run_demo.py
  └─ README.md
```

## Quick start (Jupyter terminal / Anaconda Prompt)

1. Open Jupyter terminal (or Anaconda Prompt) and navigate to the project folder:
   ```
   cd path/to/vectorclock-rpc
   ```
2. (Optional) Create & activate virtualenv:
   ```
   python -m venv venv
   source venv/bin/activate    # on Windows PowerShell: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running without Docker (dev)
1. Start server:
   ```
   python server.py
   ```
2. In a new terminal run client:
   ```
   python client.py --id A send --msg "hello from A"
   python client.py --id B send --msg "hello from B"
   ```
3. Check `.client_state/A.json` and `.client_state/B.json` for vector clocks.

## Running with Docker (recommended for submission)
1. Build the image (in Jupyter terminal):
   ```
   docker build -t vectorclock-server:latest .
   ```
2. Run the container:
   ```
   docker run -p 5000:5000 --rm --name vc-server vectorclock-server:latest
   ```
   Server will listen on http://localhost:5000

3. In another terminal (host), run clients:
   ```
   python client.py --id A send --msg "A1"
   python client.py --id B fetch-and-merge
   python client.py --id B send --msg "B_after_A"
   ```

## Automated demo
Run `python run_demo.py` — it will start server, perform causal and concurrent tests, and save logs to `demo_logs/`.

## What to include in your report
- Explanation of vector clock design (increment, merge, compare)
- Paste server logs (`demo_logs` or console) showing causal vs concurrent
- Include `.client_state/*.json` snapshots

## Deployment notes
- The Dockerfile runs the Flask app under gunicorn on port 5000.
- For cloud providers that set `PORT` env var, update gunicorn bind accordingly or use `CMD` override.

## Contact
If you want, I can also:
- generate a 2–3 page PDF report from logs
- push this to a GitHub repo and provide sample commit messages
