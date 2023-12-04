"""Used for login logic."""

from typing import Any

from aiohttp import ClientSession

import base64

from sems_portal_api.sems_region import get_region

async def login_to_sems(session: ClientSession, account: str, pwd: str) -> Any:
    """Login to the SEMS portal."""
    url = "https://www.semsportal.com/api/v1/Common/CrossLogin"
    headers = {
        "Content-Type": "application/json",
        "Token": '{"version":"v2.1.0","client":"ios","language":"en"}',
    }
    body = {"account": account, "pwd": pwd}

    response = await session.post(url, headers=headers, json=body, timeout=5)
    response_data = await response.json()

    return response_data["data"]

def login_response_to_token(login_data: Any) -> str:
    return base64.b64encode(bytes(str(login_data), 'utf-8')).decode('utf-8')

async def get_station_ids(session: ClientSession, token: str) -> Any:
    """Get the station id of an account"""
    url = f"https://{get_region()}.semsportal.com/api/PowerStation/GetPowerStationIdByOwner"
    headers = {
        "Content-Type": "application/json",
        "Token": token,
    }

    response = await session.post(url, headers=headers, timeout=5)
    response_data = await response.json()

    return response_data["data"]
