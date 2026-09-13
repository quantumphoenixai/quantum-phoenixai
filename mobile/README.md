## Dashboard API

The mobile integration is a dashboard served by a read-only local API. Start it from the project root:

```powershell
py .\src\mobile_api.py
```

Endpoints:

- `GET /health`
- `GET /api/events`
- `GET /api/alerts`
- `GET /api/summary`

Open `http://127.0.0.1:8765` for the dashboard. The default API address is `http://127.0.0.1:8765`.

