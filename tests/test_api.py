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


async def part_factory(client: AsyncClient, idx: int = 1):
    part_payload = {
        "part_number": f"TEST-PART-00{idx+1}",
        "description": f"Test part {idx+1}",
        "price": 100.0 + idx,
        "quantity": 10 + idx
    }
    response = await client.post("/parts", json=part_payload)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_list_parts(client: AsyncClient):
    for idx in range(5):
        await part_factory(client, idx)

    response = await client.get("/parts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5


@pytest.mark.asyncio
async def test_list_parts_pagination(client: AsyncClient):
    limit = 3
    for idx in range(10):
        await part_factory(client, idx)

    response = await client.get("/parts", params={"limit": limit})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == limit


@pytest.mark.asyncio
async def test_list_parts_filter(client: AsyncClient):
    for idx in range(3):
        await part_factory(client, idx)

    response = await client.get("/parts", params={"part_number": "TEST-PART-001"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["part_number"] == "TEST-PART-001"


@pytest.mark.asyncio
async def test_list_parts_order_by(client: AsyncClient):
    for idx in range(5):
        await part_factory(client, idx)

    response = await client.get("/parts", params={"order_by": "quantity", "sort": "asc"})
    assert response.status_code == 200
    data = response.json()
    for i in range(len(data) - 1):
        assert data[i]["quantity"] <= data[i + 1]["quantity"]

    response = await client.get("/parts", params={"order_by": "quantity", "sort": "desc"})
    data = response.json()

    for i in range(len(data) - 1):
        assert data[i]["quantity"] >= data[i + 1]["quantity"]


@pytest.mark.asyncio
async def test_update_part_success(client: AsyncClient):
    response = await client.post("/parts", json=valid_part_payload)
    assert response.status_code == 201

    part_id = response.json()["id"]
    update_payload = {
        "part_number": "UPDATED-PART-001",
        "description": "Updated part",
        "price": 150.0,
        "quantity": 20
    }
    response = await client.put(f"/parts/{part_id}", json=update_payload)
    assert response.status_code == 200

    data = response.json()
    for key in update_payload:
        assert update_payload[key] == data[key]
    
@pytest.mark.asyncio
async def test_update_part_not_found(client: AsyncClient):
    invalid_part_id = 999999
    update_payload = {
        "part_number": "UPDATED-PART-001",
        "description": "Updated part",
        "price": 150.0,
        "quantity": 20
    }
    response = await client.put(f"/parts/{invalid_part_id}", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Part with id '{invalid_part_id}' not found"

@pytest.mark.asyncio
async def test_update_part_with_invalid_payload(client: AsyncClient):
    response = await client.post("/parts", json=valid_part_payload)
    assert response.status_code == 201

    part_id = response.json()["id"]
    invalid_payload = {
        "part_number": None,
        "description": "Updated part",
        "price": -150.0,
        "quantity": 20
    }
    response = await client.put(f"/parts/{part_id}", json=invalid_payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

@pytest.mark.asyncio
async def test_partial_update_part_success(client: AsyncClient):
    response = await client.post("/parts", json=valid_part_payload)
    assert response.status_code == 201

    part_id = response.json()["id"]
    partial_update_payload = {
        "description": "Part with partial update"
    }
    response = await client.patch(f"/parts/{part_id}", json=partial_update_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["description"] == partial_update_payload["description"]



@pytest.mark.asyncio
async def test_delete_part_success(client: AsyncClient):
    response = await client.post("/parts", json=valid_part_payload)
    assert response.status_code == 201

    part_id = response.json()["id"]
    response = await client.delete(f"/parts/{part_id}")
    assert response.status_code == 204

    response = await client.get(f"/parts/{part_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Part with id '{part_id}' not found"

