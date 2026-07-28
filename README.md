# ZAPConnector (FastAPI)

Simple FastAPI wrapper that exposes a small API to interact with OWASP ZAP using an API key for access.

Environment variables (see `.env.example`):

- `APP_API_KEY` — API key clients must send in `X-API-Key` header.
- `ZAP_BASE_URL` — URL to the running ZAP proxy, e.g. `http://127.0.0.1:8080`.
- `ZAP_API_KEY` — (optional) ZAP's own API key if configured.

Quick start

1. Create a virtualenv and install:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `APP_API_KEY` and `ZAP_BASE_URL`.

3. Run the app:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Example request (replace `yourkey`):

```bash
curl -X POST "http://localhost:8000/scan?target=http://example.com" -H "X-API-Key: yourkey"
```
