diff --git a/backend/server.py b/backend/server.py
index 05856c57485fd7235f9cdf8879f9b7ea83983884..44cf1bd0aa9dab702c5ab25c97c4ed376affda98 100644
--- a/backend/server.py
+++ b/backend/server.py
@@ -1,75 +1,109 @@
 from fastapi import FastAPI, APIRouter
 from dotenv import load_dotenv
 from starlette.middleware.cors import CORSMiddleware
 from motor.motor_asyncio import AsyncIOMotorClient
 import os
 import logging
 from pathlib import Path
 from pydantic import BaseModel, Field
-from typing import List
+from typing import List, Dict
 import uuid
 from datetime import datetime
 
 
 ROOT_DIR = Path(__file__).parent
-load_dotenv(ROOT_DIR / '.env')
+load_dotenv(ROOT_DIR / ".env")
 
 # MongoDB connection
-mongo_url = os.environ['MONGO_URL']
+mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
+db_name = os.getenv("DB_NAME", "zimzima")
 client = AsyncIOMotorClient(mongo_url)
-db = client[os.environ['DB_NAME']]
+db = client[db_name]
 
 # Create the main app without a prefix
 app = FastAPI()
 
 # Create a router with the /api prefix
 api_router = APIRouter(prefix="/api")
 
 
 # Define Models
+
+
 class StatusCheck(BaseModel):
     id: str = Field(default_factory=lambda: str(uuid.uuid4()))
     client_name: str
     timestamp: datetime = Field(default_factory=datetime.utcnow)
 
+
 class StatusCheckCreate(BaseModel):
     client_name: str
 
+
+class Lead(BaseModel):
+    name: str
+    company: str
+    city: str
+    contact: str
+    source: str
+
+
 # Add your routes to the router instead of directly to app
+
+
 @api_router.get("/")
 async def root():
     return {"message": "Hello World"}
 
+
 @api_router.post("/status", response_model=StatusCheck)
 async def create_status_check(input: StatusCheckCreate):
     status_dict = input.dict()
     status_obj = StatusCheck(**status_dict)
     _ = await db.status_checks.insert_one(status_obj.dict())
     return status_obj
 
+
 @api_router.get("/status", response_model=List[StatusCheck])
 async def get_status_checks():
     status_checks = await db.status_checks.find().to_list(1000)
     return [StatusCheck(**status_check) for status_check in status_checks]
 
+
+@api_router.get("/scraper/run_all")
+async def run_all(city: str, business_type: str) -> Dict[str, List[Lead]]:
+    """Return dummy leads for now."""
+    dummy_lead = Lead(
+        name="John Doe",
+        company="Acme Inc",
+        city=city,
+        contact="john@example.com",
+        source="dummy",
+    )
+    return {"linkedin": [dummy_lead], "zillow": [], "businesses": []}
+
+
 # Include the router in the main app
 app.include_router(api_router)
 
+
 app.add_middleware(
     CORSMiddleware,
     allow_credentials=True,
     allow_origins=["*"],
     allow_methods=["*"],
     allow_headers=["*"],
 )
 
+
 # Configure logging
 logging.basicConfig(
     level=logging.INFO,
-    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
+    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
 )
 logger = logging.getLogger(__name__)
 
+
 @app.on_event("shutdown")
 async def shutdown_db_client():
     client.close()

