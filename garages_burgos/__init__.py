"""Fetch latest parking garage information from Burgos."""
import logging
from dataclasses import dataclass

from aiohttp import ClientSession


@dataclass
class Garage:
    """Class for garages Burgos"""

    URL = "https://movilidad.aytoburgos.es/o/aytoburgos-movilidad-ws/parkingStatus?groupId=413443"
    NAME = "Garage Burgos"

    name: str
    state: str
    free_space: int
    total_capacity: int

    @staticmethod
    def from_json(item):
        free_space = int(item["free_space"])
        total_capacity = int(item["total_space"])
        free_percentage = free_space / total_capacity
        return Garage(
            name=fix_encoding(item["name"]),
            state="Available" if free_percentage > 0.1 else "Complete",
            free_space=free_space,
            total_capacity=total_capacity,
        )


DEFAULT_SOURCE = Garage


def fix_encoding(str):
    return str.replace("Espa�a", "España").replace("Evoluci�n", "Evolución")


async def get_garages(session: ClientSession, *, source=DEFAULT_SOURCE):
    """Fetch parking garage data."""
    try:
        response = await session.get(source.URL)
        json = await response.json()
        data = json['data']
        results = []
        for parking in data:
            name = parking['4']
            free = parking['1']
            total = parking['3']
            json = {"name": name, "free_space": free, "total_space": total}
            results.append(source.from_json(json))
        return results
    except RuntimeError:
        logging.getLogger(__name__).warning("Cannot get data")
        return []
