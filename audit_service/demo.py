import asyncio
import httpx
import uuid
import random
from datetime import datetime

# Configuration
API_URL = "http://68.183.88.205/v1/audit"  # Change to your Droplet IP when deployed e.g., http://<droplet_ip>/v1/audit

async def demo_audit_flow():
    print(f"🚀 Starting Audit Service Demo against {API_URL}")
    print("-" * 60)

    async with httpx.AsyncClient() as client:
        # 1. Simulate a successful User Login
        await send_log(client, {
            "service_name": "auth-service",
            "action": "LOGIN",
            "entity_type": "User",
            "entity_id": "usr_123",
            "performed_by": "usr_123",
            "performed_by_ip": "192.168.1.10",
            "success": True,
            "context": {"method": "password", "browser": "Chrome"}
        })

        # 2. Simulate Order Creation
        await send_log(client, {
            "service_name": "order-service",
            "action": "CREATE",
            "entity_type": "Order",
            "entity_id": f"ORD-{random.randint(1000, 9999)}",
            "performed_by": "usr_123",
            "new_value": {"total": 450.00, "items": 3},
            "success": True
        })

        # 3. Simulate a Failed Payment
        await send_log(client, {
            "service_name": "payment-service",
            "action": "EXECUTE",
            "entity_type": "Payment",
            "performed_by": "system",
            "success": False,
            "error_message": "Insufficient funds",
            "context": {"gateway": "Stripe"}
        })

    print("-" * 60)
    print("✨ Demo complete! Check the server logs (docker logs) to see the stored records.")

async def send_log(client, data):
    try:
        response = await client.post(
            API_URL,
            json=data,
            headers={"X-Request-ID": str(uuid.uuid4())}
        )
        response.raise_for_status()
        result = response.json()
        print(f"✅ [{data['action']}] Logged ID: {result['id']} (Time: {result['timestamp']})")
    except Exception as e:
        print(f"❌ Failed to log {data['action']}: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(demo_audit_flow())
    except KeyboardInterrupt:
        pass
