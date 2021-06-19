"""Fetch latest parking garage information from Burgos."""
from aiohttp import ClientSession
from dataclasses import dataclass
from bs4 import BeautifulSoup
import re

import logging


@dataclass
class Garage:
    """Class for garages Burgos"""

    URL = "http://www.aytoburgos.es/movilidad-y-transporte/mapa-aparcamientos-publicos"
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
    return str.replace("Ã³", "ó").replace("Ã±", "ñ")


async def get_garages(session: ClientSession, *, source=DEFAULT_SOURCE):
    """Fetch parking garage data."""
    try:
        response = await session.get(source.URL)
        html = await response.text(encoding='latin-1')
        bs = BeautifulSoup(html, features='lxml')
        rows = bs.find_all('tr')
        results = []
        for idx, row in enumerate(rows):
            if idx != 0:
                content = row.get_text()
                result = " ".join(content.split())
                data = re.match(r'(.+) (\d+) (\d+)', result)
                (name, free, total) = data.groups()
                json = {"name": name, "free_space": free, "total_space": total}
                results.append(source.from_json(json))
        return results
        '''
    except UnicodeDecodeError:
        logging.getLogger(__name__).warning("Cannot format data")
        return []
        '''
    except RuntimeError:
        logging.getLogger(__name__).warning("Cannot get data")
        return []
