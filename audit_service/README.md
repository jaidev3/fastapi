# Audit Service

Simple, reliable audit trail microservice built with FastAPI.

## Structure

- `app/domain`: Domain models (AuditEntry, etc.)
- `app/service`: Business logic (AuditService)
- `app/repository`: Data access interfaces and implementations
- `app/api`: HTTP controllers
- `app/settings.py`: Configuration using pydantic-settings

## Running

### Local
1. Create and activate virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker
1. Build:
   ```bash
   docker build -t audit-service .
   ```
2. Run:
   ```bash
   docker run -p 8000:8000 audit-service
   ```
### Test Api
1. From Swagger UI (Manual Testing)
   Open your browser and navigate to: `http://localhost:8000/docs`

2. Open `demo.py` and update the `API_URL` variable at the top:
   ```python
   API_URL = "http://localhost:8000/v1/audit"
   ```
3. Run the script:
   ```bash
   pip install httpx asyncio
   python demo.py
   ```

4. Deployed Api
   Open your browser and navigate to: `http://<YOUR_DROPLET_IP>/docs`

   