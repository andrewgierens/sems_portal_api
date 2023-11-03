"""Used for getting sems charts data."""

from datetime import datetime
from typing import Any

from aiohttp import ClientSession


async def get_plant_power_chart(
    session: ClientSession, plant_id: str, token: str, targetDate: datetime = datetime.now()
) -> Any:
    """Retrieve powerplant chart data."""
    formatted_date = targetDate.strftime("%Y-%m-%d")
    url = "https://au.semsportal.com/api/v2/Charts/GetPlantPowerChart"
    headers = {"Content-Type": "application/json", "Token": token}
    body = {"id": plant_id, "date": formatted_date, "full_script": False}

    response = await session.post(url, headers=headers, json=body, timeout=5)
    response_data = await response.json()

    return response_data["data"]
