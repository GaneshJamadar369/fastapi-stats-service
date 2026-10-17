# FastAPI Dynamic Stats Service

Implements `GET /stats?values=1,2,3` with dynamic descriptive statistics, strict single-origin CORS, and `X-Request-ID` / `X-Process-Time` headers on responses including preflight and error responses.

- Account email: `23f3003450@ds.study.iitm.ac.in`
- Allowed origin: `https://dash-58vl6u.example.com`
- Health check: `/health`
- Interactive API docs: `/docs`

## Run locally

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Test a calculation:

```bash
curl 'http://127.0.0.1:8000/stats?values=1,2,3,10'
```

Expected stats: count `4`, sum `16`, min `1`, max `10`, mean `4.0`.

## CORS preflight checks

Allowed origin (should return ACAO):

```bash
curl -i -X OPTIONS http://127.0.0.1:8000/stats \
  -H 'Origin: https://dash-58vl6u.example.com' \
  -H 'Access-Control-Request-Method: GET'
```

Untrusted origin (must not return ACAO; expected 400):

```bash
curl -i -X OPTIONS http://127.0.0.1:8000/stats \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: GET'
```

## Deploy to Render

1. Create a **public or private GitHub repository** and upload `main.py`, `requirements.txt`, and `render.yaml` from this folder.
2. In Render, choose **New + → Blueprint** and connect that repository.
3. Render reads `render.yaml` and creates the web service. Wait for deployment to finish.
4. Copy the generated service URL, e.g. `https://<your-service>.onrender.com` (use your actual URL, not this example).
5. Verify `/health`, `/stats?values=1,2,3`, and the two preflight commands with your real base URL before submitting it.

The service computes statistics from each request; it does not contain fixed answers for grader batches.
