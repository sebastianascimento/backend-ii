from fastapi import FastAPI
import asyncio
import time
from datetime import datetime

app = FastAPI()

async def fetch_user_data():
    """Simulate fetching user data from database"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting user data fetch")
    await asyncio.sleep(2)  
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed user data fetch")
    return {
        "users_total": 842,
        "users_active": 127,
        "new_signups_today": 34
    }

async def fetch_metrics_data():
    """Simulate fetching analytics data from metrics service"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting metrics data fetch")
    await asyncio.sleep(1.5)  
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed metrics data fetch")
    return {
        "page_views": 12750,
        "unique_visitors": 3840,
        "avg_session_time": 187  
    }

@app.get("/dashboard")
async def get_dashboard_data():
    """Dashboard endpoint that concurrently fetches data from two sources"""
    start_time = time.time()
    
    user_data, metrics_data = await asyncio.gather(
        fetch_user_data(),
        fetch_metrics_data()
    )
    
    execution_time = time.time() - start_time
    
    return {
        "timestamp": datetime.now().isoformat(),
        "execution_time_seconds": round(execution_time, 3),
        "data": {
            "user_statistics": user_data,
            "site_metrics": metrics_data
        }
    }

@app.get("/")
async def root():
    return {"message": "API is running! Go to /dashboard for concurrent data"}