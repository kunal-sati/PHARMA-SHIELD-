from fastapi import APIRouter, HTTPException

from backend.app.integrations.sap_odata import sap_odata_client


router = APIRouter(
    prefix="/sap",
    tags=["SAP Integration"],
)


@router.get("/shipments")
async def get_sap_shipments():
    try:
        return await sap_odata_client.get_shipments()
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"SAP OData request failed: {exc}",
        ) from exc