import aiohttp
import asyncio

import garages_burgos


async def main():
    """Simple function to test the output."""
    async with aiohttp.ClientSession() as client:
        result = await garages_burgos.get_garages(client)
        return result


async def basic():
    result = await main()
    assert len(result) == 4


async def parking():
    all_data = await main()
    matches = next(x for x in all_data if x.name == "Plaza Vega - Catedral")
    assert matches.name == "Plaza Vega - Catedral"
    assert matches.state == "Available"
    assert type(matches.free_space) is int
    assert type(matches.total_capacity) is int


async def encoding():
    all_data = await main()
    print(all_data)
    iterator1 = (x for x in all_data if x.name == "Museo Evolución Humana")
    iterator2 = (x for x in all_data if x.name == "Plaza España")
    try:
        next(iterator1)
        next(iterator2)
    except StopIteration:
        assert False
    assert True


def test_basic():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(basic())


def test_parking():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parking())


def test_encoding():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(encoding())
