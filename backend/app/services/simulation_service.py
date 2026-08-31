import uuid
import datetime
from sqlalchemy.orm import Session
from backend.app.models.entities import (
    Organization, Shipment, SensorReading, User, Disruption, Recommendation, Approval, AuditLog,
    Facility, Product, Supplier, RouteMaster, Policy, HistoricalIncident, KnowledgeDocument, Notification, Incident
)
from backend.app.core.security import hash_password

class SimulationService:
    NORMAL_TEMPS = [4.2, 4.4, 4.5, 4.7, 4.8]
    EXCURSION_TEMPS = [5.2, 6.1, 7.3, 8.1, 8.9, 9.6]
    RECOVERY_TEMPS = [8.2, 6.5, 5.1, 4.5, 4.2]

    @classmethod
    def seed_initial_data(cls, db: Session):
        """Seed baseline shipments, master data, demo users, policies, RAG knowledge, and initial sensor history."""

        # 1. Seed Organization
        if not db.query(Organization).filter_by(id="ORG-DEMO").first():
            org = Organization(id="ORG-DEMO", name="PharmaShield Demo Organization", tenant_code="TENANT-DEMO")
            db.add(org)
            db.commit()

        # 2. Seed Users
        if not db.query(User).filter_by(id="USR-001").first():
            users = [
                User(id="USR-001", organization_id="ORG-DEMO", name="Alex Turner", email="operator@pharmashield.io", role="OPERATOR", password_hash=hash_password("Password123!")),
                User(id="USR-002", organization_id="ORG-DEMO", name="Sarah Connor", email="manager@pharmashield.io", role="MANAGER", password_hash=hash_password("Password123!")),
                User(id="USR-003", organization_id="ORG-DEMO", name="David Miller", email="auditor@pharmashield.io", role="AUDITOR", password_hash=hash_password("Password123!")),
                User(id="USR-004", organization_id="ORG-DEMO", name="Elena Rostova", email="admin@pharmashield.io", role="ADMIN", password_hash=hash_password("Password123!"))
            ]
            db.add_all(users)
            db.commit()

        # 3. Seed Master Data: Facilities
        if not db.query(Facility).filter_by(facility_id="CS-04").first():
            facilities = [
                Facility(facility_id="CS-01", name="Delhi Central Cold Logistics Hub #1", location_name="Delhi", facility_type="HUB", latitude=28.7041, longitude=77.1025, total_capacity_units=1500, available_capacity_units=450, operating_temp=4.0, status="ONLINE"),
                Facility(facility_id="CS-04", name="Northern Regional Cold Storage Depot #4", location_name="Ambala", facility_type="COLD_STORAGE", latitude=28.7841, longitude=77.1425, total_capacity_units=800, available_capacity_units=122, operating_temp=3.9, status="ONLINE"),
                Facility(facility_id="CS-07", name="Chandigarh Biologics Receiving Hub #7", location_name="Chandigarh", facility_type="REGIONAL_DEPOT", latitude=30.7333, longitude=76.7794, total_capacity_units=1000, available_capacity_units=300, operating_temp=4.2, status="ONLINE")
            ]
            db.add_all(facilities)
            db.commit()

        # 4. Seed Master Data: Products
        if not db.query(Product).filter_by(product_id="VAX-001").first():
            products = [
                Product(product_id="VAX-001", name="Vaccine", category="Temperature-sensitive pharmaceutical", min_temperature=2.0, max_temperature=8.0, criticality="HIGH", transport_requirements="REFRIGERATED_COLD_CHAIN", approved_facilities_json=["CS-01", "CS-04", "CS-07"]),
                Product(product_id="INS-002", name="Insulin Vials", category="Temperature-sensitive peptide", min_temperature=2.0, max_temperature=8.0, criticality="MEDIUM", transport_requirements="REFRIGERATED_COLD_CHAIN", approved_facilities_json=["CS-01", "CS-04"])
            ]
            db.add_all(products)
            db.commit()

        # 5. Seed Master Data: Suppliers & Routes
        if not db.query(Supplier).filter_by(supplier_id="SUP-001").first():
            db.add(Supplier(supplier_id="SUP-001", name="Apex Bio-Logistics", reliability_rating=98.5, historical_excursion_rate=1.2, historical_avg_delay_minutes=8.5))
            db.add(RouteMaster(route_id="RTE-DEL-CHD", name="Delhi → Chandigarh Expressway (NH-44)", origin="Delhi", destination="Chandigarh", distance_km=244.0, base_eta_minutes=270, historical_risk_score=15, traffic_risk_factor=1.2))
            db.commit()

        # 6. Seed Policy
        if not db.query(Policy).filter_by(policy_id="POL-001").first():
            db.add(Policy(policy_id="POL-001", name="Enterprise Pharmaceutical Governance Policy v2.0", description="Enforces ABAP Rules 1-5 for cold chain excursion thresholds and manager sign-off on high-impact rerouting.", min_criticality="HIGH", cost_threshold=1000.0, risk_threshold=80, action_tier="HIGH", requires_approval=True, is_active=True))
            db.commit()

        # 7. Seed Historical Incidents & SOP RAG Knowledge
        if not db.query(HistoricalIncident).filter_by(id="HIST-001").first():
            db.add(HistoricalIncident(id="HIST-001", title="Summer Heatwave Excursion on NH-44", symptoms="Vehicle refrigeration compressor pressure drop under 42°C ambient heat; temp reached 9.4°C", product_category="Vaccine", selected_action="REROUTE_TO_COLD_STORAGE", outcome="RECOVERED_SUCCESS", recovery_duration_minutes=24, lessons_learned="Immediate rerouting to Depot CS-04 preserved 100% thermal integrity without potency degradation."))
            db.add(KnowledgeDocument(id="KNOW-001", title="PharmaShield Cold Storage Ingestion SOP v2.1", category="SOP", source_uri="sop://pharmashield/cold-chain-ingestion", content="Standard Operating Procedure for Pharmaceutical Cold Storage Rerouting: All biologics and vaccines exceeding maximum threshold 8.0°C for over 15 minutes MUST be transferred to approved cold storage facility CS-04 or CS-07. Human Manager approval is mandatory if transfer cost exceeds ₹1,000."))
            db.commit()

        # 8. Seed Baseline Shipments
        if not db.query(Shipment).filter_by(shipment_id="PS-1026").first():
            shipments = [
                Shipment(
                    shipment_id="PS-1024",
                    organization_id="ORG-DEMO",
                    product_id="VAX-001",
                    product_name="Oncology Biologics",
                    product_type="Monoclonal Antibodies",
                    origin="Mumbai",
                    destination="Pune",
                    min_temperature=2.0,
                    max_temperature=8.0,
                    criticality="MEDIUM",
                    quantity_units=300,
                    current_status="NORMAL",
                    current_temperature=5.1,
                    current_latitude=19.0760,
                    current_longitude=72.8777,
                    delay_minutes=0,
                    traffic_level="NORMAL"
                ),
                Shipment(
                    shipment_id="PS-1025",
                    organization_id="ORG-DEMO",
                    product_id="INS-002",
                    product_name="Insulin Vials",
                    product_type="Temperature-sensitive peptide",
                    origin="Bengaluru",
                    destination="Hyderabad",
                    min_temperature=2.0,
                    max_temperature=8.0,
                    criticality="MEDIUM",
                    quantity_units=400,
                    current_status="WARNING",
                    current_temperature=7.8,
                    current_latitude=12.9716,
                    current_longitude=77.5946,
                    delay_minutes=15,
                    traffic_level="MODERATE"
                ),
                Shipment(
                    shipment_id="PS-1026",
                    organization_id="ORG-DEMO",
                    product_id="VAX-001",
                    product_name="Vaccine",
                    product_type="Temperature-sensitive pharmaceutical",
                    origin="Delhi",
                    destination="Chandigarh",
                    min_temperature=2.0,
                    max_temperature=8.0,
                    criticality="HIGH",
                    quantity_units=500,
                    current_status="IN_TRANSIT",
                    current_temperature=4.2,
                    current_latitude=28.7041,
                    current_longitude=77.1025,
                    delay_minutes=47,
                    traffic_level="HIGH"
                )
            ]
            db.add_all(shipments)
            db.commit()

            # Seed initial normal sensor readings for PS-1026
            now = datetime.datetime.now(datetime.timezone.utc)
            for i, temp in enumerate(cls.NORMAL_TEMPS):
                reading = SensorReading(
                    id=f"SR-{uuid.uuid4().hex[:8].upper()}",
                    shipment_id="PS-1026",
                    timestamp=now - datetime.timedelta(minutes=(5 - i) * 5),
                    temperature=temp,
                    humidity=52.0,
                    latitude=28.7041 + (i * 0.01),
                    longitude=77.1025 + (i * 0.01),
                    speed=42.0,
                    traffic_level="HIGH"
                )
                db.add(reading)
            db.commit()

    @classmethod
    def reset_scenario(cls, db: Session, shipment_id: str = "PS-1026"):
        """Reset shipment PS-1026 to baseline state."""
        shipment = db.query(Shipment).filter_by(shipment_id=shipment_id).first()
        if shipment:
            shipment.current_status = "NORMAL"
            shipment.current_temperature = 4.2
            shipment.delay_minutes = 47
            shipment.traffic_level = "HIGH"
            shipment.current_latitude = 28.7041
            shipment.current_longitude = 77.1025

            # Clear associated disruptions, recommendations, approvals, audit records for clean demo
            db.query(Approval).filter_by(shipment_id=shipment_id).delete()
            db.query(Recommendation).filter_by(shipment_id=shipment_id).delete()
            db.query(Disruption).filter_by(shipment_id=shipment_id).delete()
            db.query(Incident).filter_by(shipment_id=shipment_id).delete()
            db.query(AuditLog).filter_by(shipment_id=shipment_id).delete()
            db.query(SensorReading).filter_by(shipment_id=shipment_id).delete()

            now = datetime.datetime.now(datetime.timezone.utc)
            for i, temp in enumerate(cls.NORMAL_TEMPS):
                reading = SensorReading(
                    id=f"SR-{uuid.uuid4().hex[:8].upper()}",
                    shipment_id=shipment_id,
                    timestamp=now - datetime.timedelta(minutes=(5 - i) * 5),
                    temperature=temp,
                    humidity=52.0,
                    latitude=28.7041 + (i * 0.01),
                    longitude=77.1025 + (i * 0.01),
                    speed=42.0,
                    traffic_level="HIGH"
                )
                db.add(reading)
            db.commit()
            db.refresh(shipment)
        return shipment
