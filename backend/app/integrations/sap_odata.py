from typing import Any

import httpx

from backend.app.core.config import settings


class SAPODataClient:
    def __init__(self) -> None:
        self.base_url = settings.SAP_ODATA_BASE_URL.rstrip("/")
        self.username = settings.SAP_USER
        self.password = settings.SAP_PASSWORD

    async def get_shipments(self) -> dict[str, Any]:
        url = f"{self.base_url}/PS_SHIPMENTSet"

        auth = None

        if self.username and self.password:
            auth = httpx.BasicAuth(
                self.username,
                self.password,
            )

        async with httpx.AsyncClient(
            timeout=15.0,
            verify=True,
        ) as client:
            response = await client.get(
                url,
                params={"$format": "json"},
                auth=auth,
            )

        response.raise_for_status()
        return response.json()


sap_odata_client = SAPODataClient()