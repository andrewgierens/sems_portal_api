from typing import Any
import re
from aiohttp import ClientSession

from sems_portal_api.sems_plant_details import get_powerflow, get_plant_details, get_inverter_details

def get_value_by_key(array_of_dicts, key_to_find):
    return next((dct["value"] for dct in array_of_dicts if dct["key"] == key_to_find), None)

def get_value_by_target_key(array_of_dicts, key_to_find):
    return next((dct["value"] for dct in array_of_dicts if dct["target_key"] == key_to_find), None)

def extract_number(s):
    """Remove units from string and turn to number."""

    # Match one or more digits at the beginning of the string
    match = re.match(r"(\d+)", s)
    if match:
        return int(match.group(1))

    return None

async def get_colated_plant_details(
    session: ClientSession, power_station_id: str, token: str
) -> Any:
    """Get powerplant details."""

    plant_information = await get_powerflow(
        session=session,
        power_station_id=power_station_id,
        token=token,
    )

    plantDetails = await get_plant_details(
        session=session,
        power_station_id=power_station_id,
        token=token,
    )

    inverterDetails = await get_inverter_details(
        session=session,
        power_station_id=power_station_id,
        token=token,
    )

    data: [str, Any] = {}

    data = {
        "powerPlant": {
            "info": {
                "name": plantDetails["info"]["stationname"],
                "model": "GoodWe",
                "powerstation_id": plantDetails["info"]["powerstation_id"],
                "stationname": plantDetails["info"]["stationname"],
                "battery_capacity": plantDetails["info"]["battery_capacity"],
                "capacity": plantDetails["info"]["capacity"],
                "monthGeneration": plantDetails["kpi"]["month_generation"],
                "generationToday": plantDetails["kpi"]["power"],
                "allTimeGeneration": plantDetails["kpi"]["total_power"],
                "todayIncome": plantDetails["kpi"]["day_income"],
                "totalIncome": plantDetails["kpi"]["total_income"],
                "generationLive": extract_number(
                    plant_information["powerflow"]["pv"]
                ),
                "pvStatus": plant_information["powerflow"]["pvStatus"],
                "battery": extract_number(
                    plant_information["powerflow"]["bettery"]
                ),
                "batteryStatus": plant_information["powerflow"]["betteryStatus"],
                "batteryStatusStr": plant_information["powerflow"][
                    "betteryStatusStr"
                ],
                "houseLoad": extract_number(plant_information["powerflow"]["load"]),
                "houseLoadStatus": plant_information["powerflow"]["loadStatus"],
                "gridLoad": extract_number(plant_information["powerflow"]["grid"]),
                "gridLoadStatus": plant_information["powerflow"]["gridStatus"],
                "soc": plant_information["powerflow"]["soc"],
                "socText": extract_number(
                    plant_information["powerflow"]["socText"]
                ),
            },
            "inverters": [{
                "name": inverter["sn"],
                "model": get_value_by_key(inverter["dict"]["left"], "dmDeviceType"),
                "innerTemp": get_value_by_key(inverter["dict"]["right"], "innerTemp"),
            } for inverter in inverterDetails],
        }
    }

    return data
