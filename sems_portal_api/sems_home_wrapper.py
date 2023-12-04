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
    match = re.match(r"(\d+(\.\d+))", s)
    if match:
        return float(match.group(1))

    return None

async def get_collated_plant_details(
    session: ClientSession, power_station_id: str, token: str
) -> Any:
    """Get powerplant details."""

    plant_information = await get_powerflow(
        session=session,
        power_station_id=power_station_id,
        token=token,
    )
    powerflow_information = plant_information["powerflow"]

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
            },
            "inverters": [{
                "name": inverter["sn"],
                "model": get_value_by_key(inverter["dict"]["left"], "dmDeviceType"),
                "innerTemp": get_value_by_key(inverter["dict"]["right"], "innerTemp"),
            } for inverter in inverterDetails],
        }
    }

    if powerflow_information is not None:
        data["powerPlant"]["info"].update({
            "generationLive": extract_number(
                powerflow_information["pv"]
            ),
            "pvStatus": powerflow_information["pvStatus"],
            "battery": extract_number(
                powerflow_information["bettery"]
            ),
            "batteryStatus": powerflow_information["betteryStatus"],
            "batteryStatusStr": powerflow_information[
                "betteryStatusStr"
            ],
            "houseLoad": extract_number(powerflow_information["load"]),
            "houseLoadStatus": powerflow_information["loadStatus"],
            "gridLoad": extract_number(powerflow_information["grid"]),
            "gridLoadStatus": powerflow_information["gridStatus"],
            "soc": powerflow_information["soc"],
            "socText": extract_number(
                powerflow_information["socText"]
            ),
        })

    return data
