import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Part

valid_part_payload = {
    "part_number": "TEST-PART-001",
    "description": "Test part",
    "price": 100.0,
    "quantity": 10
}

@pytest.mark.asyncio
async def test_create_part_success(client: AsyncClient, session: AsyncSession):
    response = await client.post("/parts", json=valid_part_payload)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    for key in valid_part_payload:
        assert valid_part_payload[key] == data[key]

    # ensure if it is in the database
    part = await session.get(Part, data["id"])
    assert part is not None
    assert part.part_number == valid_part_payload["part_number"]


@pytest.mark.asyncio
async def test_create_duplicate_part(client: AsyncClient):
    response1 = await client.post("/parts", json=valid_part_payload)
    assert response1.status_code == 201

    response2 = await client.post("/parts", json=valid_part_payload)
    assert response2.status_code == 400
    assert (
        response2.json()["detail"] ==
        f"Part with part_number '{valid_part_payload['part_number']}' already exists"
    )


@pytest.mark.asyncio
async def test_create_part_with_null_part_number(client: AsyncClient):
    invalid_payload = valid_part_payload.copy()
    invalid_payload["part_number"] = None

    response = await client.post("/parts", json=invalid_payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"


@pytest.mark.asyncio
async def test_create_part_with_missing_part_number(client: AsyncClient):
    invalid_payload = valid_part_payload.copy()
    del invalid_payload["part_number"]
    
    response = await client.post("/parts", json=invalid_payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_create_part_with_negative_price(client: AsyncClient):
    invalid_payload = valid_part_payload.copy()
    invalid_payload["price"] = -10.0

    response = await client.post("/parts", json=invalid_payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be greater than or equal to 0"


@pytest.mark.asyncio
async def test_get_part_success(client: AsyncClient):
    response = await client.post("/parts", json=valid_part_payload)
    assert response.status_code == 201

    part_id = response.json()["id"]
    response = await client.get(f"/parts/{part_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_part_not_found(client: AsyncClient):
    invalid_part_id = 999999
    response = await client.get(f"/parts/{invalid_part_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Part with id '{invalid_part_id}' not found"


def test_fail():
    assert False, 'github action works :)'
