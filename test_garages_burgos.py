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
    print(
        matches.free_space, matches.total_capacity,
        matches.free_space / matches.total_capacity
    )
    assert type(matches.free_space) is int
    assert type(matches.total_capacity) is int


async def full_parking():
    all_data = await main()
    matches = next(x for x in all_data if x.name == "Plaza Vega - Catedral")
    print(
        matches.free_space, matches.total_capacity,
        matches.free_space / matches.total_capacity
    )
    assert matches.state == "Complete"


async def free_parking():
    all_data = await main()
    matches = next(x for x in all_data if x.name == "Plaza Vega - Catedral")
    print(
        matches.free_space, matches.total_capacity,
        matches.free_space / matches.total_capacity
    )
    assert matches.state == "Available"


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


def test_full_parking(mocker):
    loop = asyncio.get_event_loop()
    mockValue = [
        garages_burgos.Garage.from_json({
            "name": "Plaza Vega - Catedral",
            "free_space": 10,
            "total_space": 250
        })
    ]
    mocker.patch('garages_burgos.get_garages', return_value=mockValue)
    loop.run_until_complete(full_parking())


def test_free_parking(mocker):
    loop = asyncio.get_event_loop()
    mockValue = [
        garages_burgos.Garage.from_json({
            "name": "Plaza Vega - Catedral",
            "free_space": 100,
            "total_space": 250
        })
    ]
    mocker.patch('garages_burgos.get_garages', return_value=mockValue)
    loop.run_until_complete(free_parking())


def test_encoding():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(encoding())
