import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tenant_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=utcnow)

    users = relationship("User", back_populates="organization")
    shipments = relationship("Shipment", back_populates="organization")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)
    criticality = Column(String, nullable=False) # LOW, MEDIUM, HIGH
    transport_requirements = Column(String, default="REFRIGERATED_COLD_CHAIN")
    handling_notes = Column(Text, nullable=True)
    approved_facilities_json = Column(JSON, nullable=True) # List of facility IDs e.g. ["CS-01", "CS-04"]


class Facility(Base):
    __tablename__ = "facilities"

    facility_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location_name = Column(String, nullable=False)
    facility_type = Column(String, nullable=False) # REGIONAL_DEPOT, COLD_STORAGE, HUB
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    total_capacity_units = Column(Integer, nullable=False, default=800)
    available_capacity_units = Column(Integer, nullable=False, default=122)
    reserved_capacity_units = Column(Integer, nullable=False, default=0)
    operating_temp = Column(Float, nullable=False, default=3.9)
    status = Column(String, nullable=False, default="ONLINE") # ONLINE, DEGRADED, OFFLINE
    supported_products_json = Column(JSON, nullable=True)


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    reliability_rating = Column(Float, default=98.5) # %
    historical_excursion_rate = Column(Float, default=1.2) # %
    historical_avg_delay_minutes = Column(Float, default=8.5)
    status = Column(String, default="APPROVED")


class RouteMaster(Base):
    __tablename__ = "routes_master"

    route_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False) # Delhi -> Chandigarh (NH-44)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
    base_eta_minutes = Column(Integer, nullable=False)
    historical_risk_score = Column(Integer, default=15)
    traffic_risk_factor = Column(Float, default=1.2)


class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id = Column(String, primary_key=True, index=True)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True, default="ORG-DEMO")
    product_id = Column(String, ForeignKey("products.product_id"), nullable=True)
    product_name = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)
    criticality = Column(String, nullable=False) # LOW, MEDIUM, HIGH
    quantity_units = Column(Integer, default=500)
    current_status = Column(String, nullable=False, default="NORMAL")
    current_temperature = Column(Float, nullable=False)
    current_latitude = Column(Float, nullable=False)
    current_longitude = Column(Float, nullable=False)
    delay_minutes = Column(Integer, default=0)
    traffic_level = Column(String, default="NORMAL")
    
    # Digital Twin & Predictive Extensions
    projected_risk_score = Column(Integer, default=0)
    time_to_critical_minutes = Column(Integer, default=120)
    product_health_pct = Column(Float, default=100.0)
    projected_loss_amount = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    organization = relationship("Organization", back_populates="shipments")
    readings = relationship("SensorReading", back_populates="shipment", cascade="all, delete-orphan")
    disruptions = relationship("Disruption", back_populates="shipment", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="shipment", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="shipment", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="shipment", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="shipment", cascade="all, delete-orphan")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(String, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    timestamp = Column(DateTime, default=utcnow)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, default=50.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, default=40.0)
    traffic_level = Column(String, default="NORMAL")

    shipment = relationship("Shipment", back_populates="readings")


class Disruption(Base):
    __tablename__ = "disruptions"

    id = Column(String, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    detected_at = Column(DateTime, default=utcnow)
    status = Column(String, default="ACTIVE")
    reason = Column(Text, nullable=False)

    shipment = relationship("Shipment", back_populates="disruptions")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False, default="DETECTED")
    owner = Column(String, default="Cold Chain Operations Center")
    sla_minutes = Column(Integer, default=30)
    reason = Column(Text, nullable=False)
    root_cause_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    shipment = relationship("Shipment", back_populates="incidents")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    scenario_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    estimated_time_minutes = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    risk_reduction = Column(String, default="Significant")
    confidence = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=False)
    why_this_action = Column(Text, nullable=True)
    why_not_alternatives = Column(Text, nullable=True)
    target_facility_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    shipment = relationship("Shipment", back_populates="recommendations")
    approvals = relationship("Approval", back_populates="recommendation")


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(String, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    recommendation_id = Column(String, ForeignKey("recommendations.id"), nullable=False)
    requested_at = Column(DateTime, default=utcnow)
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(String, nullable=True)
    status = Column(String, nullable=False, default="PENDING")
    comments = Column(Text, nullable=True)

    shipment = relationship("Shipment", back_populates="approvals")
    recommendation = relationship("Recommendation", back_populates="approvals")


class Policy(Base):
    __tablename__ = "policies"

    policy_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    min_criticality = Column(String, default="HIGH")
    cost_threshold = Column(Float, default=1000.0)
    risk_threshold = Column(Integer, default=80)
    action_tier = Column(String, default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    requires_approval = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)


class HistoricalIncident(Base):
    __tablename__ = "historical_incidents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    symptoms = Column(Text, nullable=False)
    product_category = Column(String, nullable=False)
    selected_action = Column(String, nullable=False)
    outcome = Column(String, nullable=False) # RECOVERED_SUCCESS, SPOILED
    recovery_duration_minutes = Column(Integer, nullable=False)
    lessons_learned = Column(Text, nullable=False)


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False) # SOP, POLICY, REGULATORY, FACILITY
    source_uri = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False) # CRITICAL_ALERT, WARNING, APPROVAL_REQUIRED, RECOVERY_STARTED, RECOVERY_COMPLETED, SECURITY_ALERT
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    shipment_id = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    shipment_id = Column(String, ForeignKey("shipments.shipment_id"), nullable=False)
    correlation_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=utcnow)
    actor = Column(String, nullable=False)
    actor_type = Column(String, nullable=False)
    agent = Column(String, nullable=True)
    event_type = Column(String, nullable=False)
    action = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    status = Column(String, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    
    previous_event_hash = Column(String, nullable=True)
    current_event_hash = Column(String, nullable=True)

    shipment = relationship("Shipment", back_populates="audit_logs")


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=True, default="ORG-DEMO")
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False) # OPERATOR, MANAGER, AUDITOR, ADMIN
    password_hash = Column(String, nullable=False)

    organization = relationship("Organization", back_populates="users")
