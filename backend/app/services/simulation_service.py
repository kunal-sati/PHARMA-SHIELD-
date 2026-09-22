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

        # 3. Seed Master Data: Facilities (10 Cold Chain Hubs across India)
        if not db.query(Facility).filter_by(facility_id="CS-01").first():
            facilities = [
                Facility(facility_id="CS-01", name="Delhi Central Cold Logistics Hub #1", location_name="Delhi", facility_type="HUB", latitude=28.7041, longitude=77.1025, total_capacity_units=1500, available_capacity_units=450, operating_temp=4.0, status="ONLINE"),
                Facility(facility_id="CS-02", name="Mumbai Port Cryo Depot #2", location_name="Mumbai", facility_type="HUB", latitude=19.0760, longitude=72.8777, total_capacity_units=2000, available_capacity_units=820, operating_temp=3.8, status="ONLINE"),
                Facility(facility_id="CS-03", name="Bengaluru Bio-Park Vault #3", location_name="Bengaluru", facility_type="HUB", latitude=12.9716, longitude=77.5946, total_capacity_units=1800, available_capacity_units=640, operating_temp=4.1, status="ONLINE"),
                Facility(facility_id="CS-04", name="Northern Regional Cold Storage Depot #4", location_name="Ambala", facility_type="COLD_STORAGE", latitude=28.7841, longitude=77.1425, total_capacity_units=800, available_capacity_units=122, operating_temp=3.9, status="ONLINE"),
                Facility(facility_id="CS-05", name="Pune Expressway Cold Storage Depot #5", location_name="Lonavala", facility_type="COLD_STORAGE", latitude=18.7557, longitude=73.4091, total_capacity_units=750, available_capacity_units=310, operating_temp=4.0, status="ONLINE"),
                Facility(facility_id="CS-06", name="Hyderabad Genome Valley Depot #6", location_name="Hyderabad", facility_type="HUB", latitude=17.3850, longitude=78.4867, total_capacity_units=1600, available_capacity_units=510, operating_temp=3.7, status="ONLINE"),
                Facility(facility_id="CS-07", name="Chandigarh Biologics Receiving Hub #7", location_name="Chandigarh", facility_type="REGIONAL_DEPOT", latitude=30.7333, longitude=76.7794, total_capacity_units=1000, available_capacity_units=300, operating_temp=4.2, status="ONLINE"),
                Facility(facility_id="CS-08", name="Chennai Port Cold Logistics Depot #8", location_name="Chennai", facility_type="REGIONAL_DEPOT", latitude=13.0827, longitude=80.2707, total_capacity_units=1200, available_capacity_units=410, operating_temp=4.3, status="ONLINE"),
                Facility(facility_id="CS-09", name="Jaipur Highway Cold Vault #9", location_name="Jaipur", facility_type="COLD_STORAGE", latitude=26.9124, longitude=75.7873, total_capacity_units=900, available_capacity_units=280, operating_temp=3.9, status="ONLINE"),
                Facility(facility_id="CS-10", name="Kolkata Eastern Logistics Depot #10", location_name="Kolkata", facility_type="HUB", latitude=22.5726, longitude=88.3639, total_capacity_units=1400, available_capacity_units=490, operating_temp=4.1, status="ONLINE")
            ]
            db.add_all(facilities)
            db.commit()

        # 4. Seed Master Data: Products (6 Specialized Pharma Lines)
        if not db.query(Product).filter_by(product_id="VAX-001").first():
            products = [
                Product(product_id="VAX-001", name="COVID-19 mRNA Vaccine", category="Temperature-sensitive vaccine", min_temperature=2.0, max_temperature=8.0, criticality="HIGH", transport_requirements="REFRIGERATED_COLD_CHAIN", approved_facilities_json=["CS-01", "CS-04", "CS-07"]),
                Product(product_id="INS-002", name="Human Insulin Vials", category="Temperature-sensitive peptide", min_temperature=2.0, max_temperature=8.0, criticality="MEDIUM", transport_requirements="REFRIGERATED_COLD_CHAIN", approved_facilities_json=["CS-01", "CS-03", "CS-06"]),
                Product(product_id="ONC-003", name="Oncology Monoclonal Antibodies", category="Targeted cancer biologic", min_temperature=2.0, max_temperature=8.0, criticality="HIGH", transport_requirements="ULTRA_SAFE_REFRIGERATED", approved_facilities_json=["CS-02", "CS-05", "CS-06"]),
                Product(product_id="BLD-004", name="Cryo Blood Plasma Pack", category="Human blood component", min_temperature=-20.0, max_temperature=-15.0, criticality="HIGH", transport_requirements="FROZEN_CRYO_CHAIN", approved_facilities_json=["CS-01", "CS-02", "CS-08"]),
                Product(product_id="GEN-005", name="Gene Therapy Vector AAV9", category="Advanced therapy medicinal product", min_temperature=-80.0, max_temperature=-60.0, criticality="CRITICAL", transport_requirements="DEEP_FREEZE_LN2", approved_facilities_json=["CS-03", "CS-06"]),
                Product(product_id="IMM-006", name="Immunoglobulin G Infusion", category="Plasma-derived protein", min_temperature=2.0, max_temperature=8.0, criticality="MEDIUM", transport_requirements="STANDARD_COLD_CHAIN", approved_facilities_json=["CS-09", "CS-10"])
            ]
            db.add_all(products)
            db.commit()

        # 5. Seed Master Data: Suppliers & Routes
        if not db.query(Supplier).filter_by(supplier_id="SUP-001").first():
            db.add_all([
                Supplier(supplier_id="SUP-001", name="Apex Bio-Logistics India", reliability_rating=98.5, historical_excursion_rate=1.2, historical_avg_delay_minutes=8.5),
                Supplier(supplier_id="SUP-002", name="ColdTrans Cryo Carrier", reliability_rating=99.1, historical_excursion_rate=0.8, historical_avg_delay_minutes=5.2),
                Supplier(supplier_id="SUP-003", name="PharmaCarrier Express", reliability_rating=96.8, historical_excursion_rate=2.4, historical_avg_delay_minutes=14.1),
                Supplier(supplier_id="SUP-004", name="National MedFreight Lines", reliability_rating=97.4, historical_excursion_rate=1.8, historical_avg_delay_minutes=11.0)
            ])
            db.add_all([
                RouteMaster(route_id="RTE-DEL-CHD", name="Delhi → Chandigarh Expressway (NH-44)", origin="Delhi", destination="Chandigarh", distance_km=244.0, base_eta_minutes=270, historical_risk_score=15, traffic_risk_factor=1.2),
                RouteMaster(route_id="RTE-MUM-PUN", name="Mumbai → Pune Expressway", origin="Mumbai", destination="Pune", distance_km=148.0, base_eta_minutes=180, historical_risk_score=10, traffic_risk_factor=1.1),
                RouteMaster(route_id="RTE-BLR-HYD", name="Bengaluru → Hyderabad Highway (NH-44)", origin="Bengaluru", destination="Hyderabad", distance_km=569.0, base_eta_minutes=540, historical_risk_score=22, traffic_risk_factor=1.3),
                RouteMaster(route_id="RTE-HYD-MAA", name="Hyderabad → Chennai Highway (NH-65/NH-16)", origin="Hyderabad", destination="Chennai", distance_km=626.0, base_eta_minutes=600, historical_risk_score=18, traffic_risk_factor=1.2),
                RouteMaster(route_id="RTE-AMD-JAI", name="Ahmedabad → Jaipur Highway (NH-48)", origin="Ahmedabad", destination="Jaipur", distance_km=670.0, base_eta_minutes=660, historical_risk_score=25, traffic_risk_factor=1.4),
                RouteMaster(route_id="RTE-CCU-PAT", name="Kolkata → Patna Highway (NH-19)", origin="Kolkata", destination="Patna", distance_km=580.0, base_eta_minutes=570, historical_risk_score=28, traffic_risk_factor=1.5)
            ])
            db.commit()

        # 6. Seed Policy
        if not db.query(Policy).filter_by(policy_id="POL-001").first():
            db.add_all([
                Policy(policy_id="POL-001", name="Enterprise Pharmaceutical Governance Policy v2.0", description="Enforces ABAP Rules 1-5 for cold chain excursion thresholds and manager sign-off on high-impact rerouting.", min_criticality="HIGH", cost_threshold=1000.0, risk_threshold=80, action_tier="HIGH", requires_approval=True, is_active=True),
                Policy(policy_id="POL-002", name="Cryo Deep Freeze Emergency Protocol", description="Mandatory transfer to nearest LN2 depot within 30 minutes of compressor failure.", min_criticality="CRITICAL", cost_threshold=500.0, risk_threshold=70, action_tier="CRITICAL", requires_approval=True, is_active=True)
            ])
            db.commit()

        # 7. Seed Historical Incidents & SOP RAG Knowledge
        if not db.query(HistoricalIncident).filter_by(id="HIST-001").first():
            db.add_all([
                HistoricalIncident(id="HIST-001", title="Summer Heatwave Excursion on NH-44", symptoms="Vehicle refrigeration compressor pressure drop under 42°C ambient heat; temp reached 9.4°C", product_category="Vaccine", selected_action="REROUTE_TO_COLD_STORAGE", outcome="RECOVERED_SUCCESS", recovery_duration_minutes=24, lessons_learned="Immediate rerouting to Depot CS-04 preserved 100% thermal integrity without potency degradation."),
                HistoricalIncident(id="HIST-002", title="Monsoon Traffic Gridlock on Mumbai-Pune Expressway", symptoms="Landslide delayed reefer truck by 180 min; internal battery backup activated", product_category="Targeted cancer biologic", selected_action="REROUTE_TO_COLD_STORAGE", outcome="RECOVERED_SUCCESS", recovery_duration_minutes=18, lessons_learned="Diverted to Lonavala Depot CS-05. Battery held for 4 hours; no temperature breach recorded."),
                HistoricalIncident(id="HIST-003", title="Refrigeration Power Failure in Hyderabad Corridor", symptoms="Secondary cooling circuit fuse blew; temp spiked to 11.2°C", product_category="Temperature-sensitive peptide", selected_action="REFRIGERATION_UNIT_REPLACEMENT", outcome="RECOVERED_SUCCESS", recovery_duration_minutes=35, lessons_learned="Mobile technician replaced reefer unit at Highway Hub #6.")
            ])
            db.add_all([
                KnowledgeDocument(id="KNOW-001", title="PharmaShield Cold Storage Ingestion SOP v2.1", category="SOP", source_uri="sop://pharmashield/cold-chain-ingestion", content="Standard Operating Procedure for Pharmaceutical Cold Storage Rerouting: All biologics and vaccines exceeding maximum threshold 8.0°C for over 15 minutes MUST be transferred to approved cold storage facility CS-04 or CS-07. Human Manager approval is mandatory if transfer cost exceeds ₹1,000."),
                KnowledgeDocument(id="KNOW-002", title="Cryogenic & Biologic Excursion Protocol v1.4", category="SOP", source_uri="sop://pharmashield/cryo-protocol", content="Emergency protocol for blood plasma and gene therapy shipments: Any temperature rise above -15°C triggers immediate alert to Control Tower. Automated dry ice recharge or immediate transfer to Cryo Depot CS-02 or CS-03 must be executed within 30 minutes."),
                KnowledgeDocument(id="KNOW-003", title="ABAP Governance Rules & Approval Workflow Guide", category="GOVERNANCE", source_uri="sap://pharmashield/abap-rules", content="SAP ABAP Governance Rules 1 to 5 enforce strict compliance. Rule 3 stipulates that any reroute or replacement action costing > ₹1,000 for HIGH criticality shipments strictly requires Human Manager sign-off. Autonomous AI execution is forbidden for Tier 1 risk events."),
                KnowledgeDocument(id="KNOW-004", title="Refrigeration Unit Mobile Replacement Guide", category="MAINTENANCE", source_uri="sop://pharmashield/reefer-replacement", content="Procedure for replacing faulty reefer compressors in transit. Requires dispatch of mobile repair van or swap to backup reefer trailer. Estimated execution time: 30-45 minutes. Approved for insulin and standard biologics.")
            ])
            db.commit()

        # 8. Seed Fleet of 18 Shipments Across 6 Logistics Corridors
        if db.query(Shipment).count() != 18:
            db.query(Approval).delete()
            db.query(Recommendation).delete()
            db.query(Disruption).delete()
            db.query(Incident).delete()
            db.query(AuditLog).delete()
            db.query(SensorReading).delete()
            db.query(Shipment).delete()
            db.commit()
            shipments_data = [
                {"id": "PS-1020", "product_id": "VAX-001", "name": "COVID-19 mRNA Vaccine Batch A", "type": "Vaccine", "origin": "Delhi", "dest": "Chandigarh", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 800, "status": "NORMAL", "temp": 4.1, "lat": 29.1000, "lng": 76.9000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1021", "product_id": "INS-002", "name": "Human Insulin Vials Lot 12", "type": "Peptide", "origin": "Delhi", "dest": "Chandigarh", "min": 2.0, "max": 8.0, "crit": "MEDIUM", "qty": 450, "status": "NORMAL", "temp": 4.5, "lat": 29.4000, "lng": 76.8500, "delay": 5, "traffic": "NORMAL"},
                {"id": "PS-1022", "product_id": "ONC-003", "name": "Oncology Antibodies Batch M", "type": "Biologic", "origin": "Mumbai", "dest": "Pune", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 350, "status": "NORMAL", "temp": 4.8, "lat": 18.9800, "lng": 73.1000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1023", "product_id": "BLD-004", "name": "Cryo Plasma Units Pack B", "type": "Blood Plasma", "origin": "Mumbai", "dest": "Pune", "min": -20.0, "max": -15.0, "crit": "HIGH", "qty": 200, "status": "NORMAL", "temp": -18.2, "lat": 18.8500, "lng": 73.2500, "delay": 10, "traffic": "MODERATE"},
                {"id": "PS-1024", "product_id": "ONC-003", "name": "Oncology Monoclonal Antibodies", "type": "Biologic", "origin": "Mumbai", "dest": "Pune", "min": 2.0, "max": 8.0, "crit": "MEDIUM", "qty": 300, "status": "NORMAL", "temp": 5.1, "lat": 18.7500, "lng": 73.4000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1025", "product_id": "INS-002", "name": "Insulin Vials Reserve", "type": "Peptide", "origin": "Bengaluru", "dest": "Hyderabad", "min": 2.0, "max": 8.0, "crit": "MEDIUM", "qty": 400, "status": "WARNING", "temp": 7.8, "lat": 14.5000, "lng": 77.8000, "delay": 15, "traffic": "MODERATE"},
                {"id": "PS-1026", "product_id": "VAX-001", "name": "Vaccine Demo Shipment", "type": "Vaccine", "origin": "Delhi", "dest": "Chandigarh", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 500, "status": "IN_TRANSIT", "temp": 4.2, "lat": 28.7041, "lng": 77.1025, "delay": 47, "traffic": "HIGH"},
                {"id": "PS-1027", "product_id": "GEN-005", "name": "Gene Therapy Vector AAV9", "type": "Gene Therapy", "origin": "Bengaluru", "dest": "Hyderabad", "min": -80.0, "max": -60.0, "crit": "CRITICAL", "qty": 150, "status": "NORMAL", "temp": -72.4, "lat": 15.2000, "lng": 78.1000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1028", "product_id": "IMM-006", "name": "Immunoglobulin G Batch C", "type": "Plasma Product", "origin": "Hyderabad", "dest": "Chennai", "min": 2.0, "max": 8.0, "crit": "MEDIUM", "qty": 600, "status": "NORMAL", "temp": 4.6, "lat": 15.8000, "lng": 79.5000, "delay": 8, "traffic": "NORMAL"},
                {"id": "PS-1029", "product_id": "VAX-001", "name": "Pediatric Vaccine Fleet", "type": "Vaccine", "origin": "Hyderabad", "dest": "Chennai", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 900, "status": "NORMAL", "temp": 4.3, "lat": 14.2000, "lng": 80.0000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1030", "product_id": "ONC-003", "name": "Targeted Chemotherapy Biologics", "type": "Biologic", "origin": "Ahmedabad", "dest": "Jaipur", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 320, "status": "NORMAL", "temp": 5.0, "lat": 24.5000, "lng": 73.7000, "delay": 12, "traffic": "MODERATE"},
                {"id": "PS-1031", "product_id": "INS-002", "name": "Rapid-Acting Insulin Pack", "type": "Peptide", "origin": "Ahmedabad", "dest": "Jaipur", "min": 2.0, "max": 8.0, "crit": "MEDIUM", "qty": 550, "status": "NORMAL", "temp": 4.4, "lat": 25.8000, "lng": 74.8000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1032", "product_id": "BLD-004", "name": "Platelet & Plasma Transfusion Pack", "type": "Blood Product", "origin": "Kolkata", "dest": "Patna", "min": -20.0, "max": -15.0, "crit": "HIGH", "qty": 280, "status": "NORMAL", "temp": -17.5, "lat": 23.5000, "lng": 87.1000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1033", "product_id": "VAX-001", "name": "Rotavirus Vaccine Fleet #4", "type": "Vaccine", "origin": "Kolkata", "dest": "Patna", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 700, "status": "NORMAL", "temp": 4.7, "lat": 24.8000, "lng": 85.5000, "delay": 18, "traffic": "HIGH"},
                {"id": "PS-1034", "product_id": "ONC-003", "name": "Breast Cancer Biologic Cargo", "type": "Biologic", "origin": "Delhi", "dest": "Chandigarh", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 410, "status": "NORMAL", "temp": 4.3, "lat": 30.1000, "lng": 76.8000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1035", "product_id": "INS-002", "name": "Long-Acting Insulin Cartridges", "type": "Peptide", "origin": "Mumbai", "dest": "Pune", "min": 2.0, "max": 8.0, "crit": "MEDIUM", "qty": 620, "status": "RECOVERED", "temp": 4.2, "lat": 18.7557, "lng": 73.4091, "delay": 25, "traffic": "MODERATE"},
                {"id": "PS-1036", "product_id": "IMM-006", "name": "Rh IVIG Immunoglobulin Fleet", "type": "Biologic", "origin": "Bengaluru", "dest": "Hyderabad", "min": 2.0, "max": 8.0, "crit": "MEDIUM", "qty": 500, "status": "NORMAL", "temp": 4.9, "lat": 16.5000, "lng": 78.3000, "delay": 0, "traffic": "NORMAL"},
                {"id": "PS-1037", "product_id": "VAX-001", "name": "Polio Oral Vaccine Reserve", "type": "Vaccine", "origin": "Hyderabad", "dest": "Chennai", "min": 2.0, "max": 8.0, "crit": "HIGH", "qty": 1100, "status": "NORMAL", "temp": 4.1, "lat": 13.5000, "lng": 80.1000, "delay": 0, "traffic": "NORMAL"}
            ]

            shipments = []
            for s in shipments_data:
                shipments.append(
                    Shipment(
                        shipment_id=s["id"],
                        organization_id="ORG-DEMO",
                        product_id=s["product_id"],
                        product_name=s["name"],
                        product_type=s["type"],
                        origin=s["origin"],
                        destination=s["dest"],
                        min_temperature=s["min"],
                        max_temperature=s["max"],
                        criticality=s["crit"],
                        quantity_units=s["qty"],
                        current_status=s["status"],
                        current_temperature=s["temp"],
                        current_latitude=s["lat"],
                        current_longitude=s["lng"],
                        delay_minutes=s["delay"],
                        traffic_level=s["traffic"]
                    )
                )
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
