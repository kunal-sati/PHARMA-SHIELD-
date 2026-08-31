from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base
from backend.app.models.entities import Facility
from backend.app.core.master_data import MasterDataEngine

def test_facility_capacity_sufficient():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    fac = Facility(
        facility_id="CS-04",
        name="Ambala Depot #4",
        location_name="Ambala",
        facility_type="COLD_STORAGE",
        latitude=28.78,
        longitude=77.14,
        total_capacity_units=800,
        available_capacity_units=122,
        operating_temp=3.9,
        status="ONLINE"
    )
    db.add(fac)
    db.commit()

    res = MasterDataEngine.evaluate_facility_capacity(db, required_quantity_units=100, target_facility_id="CS-04")
    assert res["is_suitable"] is True
    assert res["available_slots"] == 122

def test_facility_capacity_insufficient():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    fac = Facility(
        facility_id="CS-04",
        name="Ambala Depot #4",
        location_name="Ambala",
        facility_type="COLD_STORAGE",
        latitude=28.78,
        longitude=77.14,
        total_capacity_units=800,
        available_capacity_units=50,
        operating_temp=3.9,
        status="ONLINE"
    )
    db.add(fac)
    db.commit()

    res = MasterDataEngine.evaluate_facility_capacity(db, required_quantity_units=500, target_facility_id="CS-04")
    assert res["is_suitable"] is False
    assert "Insufficient capacity" in res["reason"]
