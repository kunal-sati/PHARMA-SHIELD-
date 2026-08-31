from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.entities import Facility, Product, Supplier, RouteMaster

class MasterDataEngine:
    """
    PharmaShield Master Data Engine.
    Handles facility capacity checks, product constraint verification, and supplier/route risk lookups.
    """

    @classmethod
    def evaluate_facility_capacity(
        cls,
        db: Session,
        required_quantity_units: int,
        target_facility_id: str = "CS-04"
    ) -> Dict[str, Any]:
        facility = db.query(Facility).filter_by(facility_id=target_facility_id).first()
        if not facility:
            return {
                "is_suitable": False,
                "reason": f"Target facility '{target_facility_id}' not found in master database.",
                "available_slots": 0
            }

        if facility.status != "ONLINE":
            return {
                "is_suitable": False,
                "reason": f"Facility {facility.name} ({facility.facility_id}) status is '{facility.status}'.",
                "available_slots": facility.available_capacity_units
            }

        if facility.available_capacity_units < required_quantity_units:
            return {
                "is_suitable": False,
                "reason": f"Insufficient capacity at {facility.name} ({facility.facility_id}): Required {required_quantity_units} units, but only {facility.available_capacity_units} available slots.",
                "available_slots": facility.available_capacity_units,
                "required_units": required_quantity_units
            }

        return {
            "is_suitable": True,
            "facility_id": facility.facility_id,
            "facility_name": facility.name,
            "operating_temp": facility.operating_temp,
            "available_slots": facility.available_capacity_units,
            "required_units": required_quantity_units,
            "reason": f"Facility {facility.name} has sufficient capacity ({facility.available_capacity_units} available slots for {required_quantity_units} units) at {facility.operating_temp}°C."
        }
