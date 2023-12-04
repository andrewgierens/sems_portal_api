"""Used to get information about the plant."""

from typing import Any

from aiohttp import ClientSession

from sems_portal_api.sems_region import get_region


async def get_plant_details(
    session: ClientSession, power_station_id: str, token: str
) -> Any:
    """Get powerplant details."""
    url = f"https://{get_region()}.semsportal.com/api/v3/PowerStation/GetPlantDetailByPowerstationId"
    headers = {"Content-Type": "application/json", "Token": token}
    body = {"PowerStationId": power_station_id}

    response = await session.post(url, headers=headers, json=body, timeout=5)
    response_data = await response.json()

    return response_data["data"]


async def get_powerflow(
    session: ClientSession, power_station_id: str, token: str
) -> Any:
    """Get the powerflow data."""

    url = f"https://{get_region()}.semsportal.com/api/v2/PowerStation/GetPowerflow"
    headers = {"Content-Type": "application/json", "Token": token}
    body = {"PowerStationId": power_station_id}


    response = await session.post(url, headers=headers, json=body, timeout=5)
    response_data = await response.json()

    return response_data["data"]


async def get_inverter_details(
    session: ClientSession, power_station_id: str, token: str
) -> Any:
    """Get the inverter data."""

    url = f"https://{get_region()}.semsportal.com/api/v3/PowerStation/GetInverterAllPoint"
    headers = {"Content-Type": "application/json", "Token": token}
    body = {"PowerStationId": power_station_id}

    response = await session.post(url, headers=headers, json=body, timeout=5)
    response_data = await response.json()

    return response_data["data"]["inverterPoints"]
