from sems_portal_api.sems_plant_details import get_powerflow


async def get_plant_details(
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
            "inverters": [],
        }
    }

    return data

    # interters = [{
    #     "name": 'Test Inverter',
    #     "model": 'Test Inverter',
    #     "Vpv1": random.randint(1, 10),
    #     "Vpv2": random.randint(1, 10),
    #     "Ipv1": random.randint(1, 10),
    #     "Ipv2": random.randint(1, 10),
    #     "Vac1": random.randint(1, 10),
    #     "Vac2": random.randint(1, 10),
    #     "Vac3": random.randint(1, 10),
    #     "Iac1": random.randint(1, 10),
    #     "Iac2": random.randint(1, 10),
    #     "Iac3": random.randint(1, 10),
    #     "Fac1": random.randint(1, 10),
    #     "Fac2": random.randint(1, 10),
    #     "Fac3": random.randint(1, 10),
    #     "Pac": random.randint(1, 10),
    #     "Tempperature": random.randint(1, 10),
    #     "Total Generation": random.randint(1, 10)
    # }]
