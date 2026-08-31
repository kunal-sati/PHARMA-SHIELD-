from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field

# --- User & Auth Schemas ---
class UserBase(BaseModel):
    id: str
    name: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# --- Sensor Reading Schemas ---
class SensorReadingCreate(BaseModel):
    shipment_id: str
    temperature: float
    humidity: float = 50.0
    latitude: float
    longitude: float
    speed: float = 40.0
    traffic_level: str = "NORMAL"

class SensorReadingResponse(SensorReadingCreate):
    id: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Disruption Schemas ---
class DisruptionDetectionResult(BaseModel):
    disruption_detected: bool
    type: str
    severity: str  # NORMAL, WARNING, CRITICAL
    risk_score: int  # 0 to 100
    confidence: float
    reasons: list[str]

class DisruptionResponse(BaseModel):
    id: str
    shipment_id: str
    type: str
    severity: str
    risk_score: int
    detected_at: datetime
    status: str
    reason: str

    model_config = ConfigDict(from_attributes=True)


# --- Scenario & Recommendation Schemas ---
class ScenarioOption(BaseModel):
    id: str
    action: str
    estimated_time_minutes: int
    estimated_cost: float
    risk_level: str
    risk_reduction: str = "High"

class PlanningAgentOutput(BaseModel):
    scenarios: list[ScenarioOption]
    recommended_scenario_id: str
    confidence: float
    reason: str

class RecommendationResponse(BaseModel):
    id: str
    shipment_id: str
    scenario_id: str
    action: str
    estimated_cost: float
    estimated_time_minutes: int
    risk_level: str
    risk_reduction: str
    confidence: float
    reasoning: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Governance & SAP Schemas ---
class SAPValidationResult(BaseModel):
    is_valid: bool
    human_approval_required: bool
    autonomous_execution_allowed: bool
    applicable_rules: list[str]
    message: str


# --- Approval Schemas ---
class ApprovalActionRequest(BaseModel):
    comments: Optional[str] = None

class ApprovalResponse(BaseModel):
    id: str
    shipment_id: str
    recommendation_id: str
    requested_at: datetime
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    status: str  # PENDING, APPROVED, REJECTED
    comments: Optional[str] = None
    recommendation: Optional[RecommendationResponse] = None

    model_config = ConfigDict(from_attributes=True)


# --- Audit Schemas ---
class AuditLogResponse(BaseModel):
    id: str
    shipment_id: str
    correlation_id: str
    timestamp: datetime
    actor: str
    actor_type: str
    agent: Optional[str] = None
    event_type: str
    action: str
    decision: str
    status: str
    metadata_json: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


# --- Shipment Schemas ---
class ShipmentCreate(BaseModel):
    shipment_id: str
    product_name: str
    product_type: str
    origin: str
    destination: str
    min_temperature: float
    max_temperature: float
    criticality: str
    current_temperature: float
    current_latitude: float
    current_longitude: float
    delay_minutes: int = 0
    traffic_level: str = "NORMAL"

class ShipmentResponse(ShipmentCreate):
    current_status: str
    created_at: datetime
    updated_at: datetime
    disruptions: list[DisruptionResponse] = []

    model_config = ConfigDict(from_attributes=True)
