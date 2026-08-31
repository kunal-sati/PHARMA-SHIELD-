import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import engine, Base, SessionLocal
from backend.app.services.simulation_service import SimulationService
from backend.app.api import (
    auth,
    shipments,
    sensors,
    simulation,
    agents_api,
    governance,
    approvals,
    execution,
    audit,
    demo,
    websockets,
    digital_twin_api,
    incidents,
    analytics,
    simulations,
    security_api,
    health,
    master_data_api,
    pre_shipment_api,
    knowledge_api,
    policy_api,
    copilot_api,
    notifications
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    
    # Seed initial baseline data
    db = SessionLocal()
    try:
        SimulationService.seed_initial_data(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Agentic Cold Chain Resilience Platform — Final Enterprise Edition",
    version="2.5.0",
    lifespan=lifespan
)

# Enable CORS for frontend Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router, prefix="/api")
app.include_router(shipments.router, prefix="/api")
app.include_router(digital_twin_api.router, prefix="/api")
app.include_router(sensors.router, prefix="/api")
app.include_router(simulation.router, prefix="/api")
app.include_router(agents_api.router, prefix="/api")
app.include_router(governance.router, prefix="/api")
app.include_router(approvals.router, prefix="/api")
app.include_router(execution.router, prefix="/api")
app.include_router(audit.router, prefix="/api")
app.include_router(incidents.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(simulations.router, prefix="/api")
app.include_router(security_api.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(master_data_api.router, prefix="/api")
app.include_router(pre_shipment_api.router, prefix="/api")
app.include_router(knowledge_api.router, prefix="/api")
app.include_router(policy_api.router, prefix="/api")
app.include_router(copilot_api.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(demo.router, prefix="/api")
app.include_router(websockets.router)

@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "system": settings.PROJECT_NAME,
        "version": "2.5.0 Enterprise Final",
        "mode": "HACKATHON_DEMO",
        "sap_integration": settings.SAP_MODE,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
